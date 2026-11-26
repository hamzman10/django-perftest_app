from projects.models import Projects
from ref_models.models import RefEnvironnement,RefOutilTest,RefTypeTest,RefProtocole
import json
from pathlib import Path
from django.conf import settings
from django.db import connection, transaction



def get_projects():

    return Projects.objects.all().order_by('name_pr').values(
        'id_project',
        'name_pr',
        'description_pr',
        'base_url'
    )

def get_environment():
    return list(
        RefEnvironnement.objects.values(
            'id_envir',
            'desingnation_env'
        )
    )


def get_testtool():
    return list(
        RefOutilTest.objects.values(
            'id_outilt',
            'desingnation_outilt'
        )
    )
def get_typetest():
    return list(
        RefTypeTest.objects.values(
            'id_type_test',
            'code_type',
            'libelle',
            'description',
            'objectif',
            'duree_secondes',
            'nb_threads',
            'ramp_up',
            'think_time',
            'volume_donnees',
            'actif',
            'nb_threads_max',
            'nb_threads_initial'
        )
    )
def get_protocol():
    return list(
        RefProtocole.objects.values(
            'id_protocol',
            'desingnation_protocol'
        )
    )






def generate_scripts(config, id_scenario, id_project, name_project):

    # Nom sécurisé du répertoire
    safe_name = "".join(
        c if c.isalnum() or c in "-_ " else "_"
        for c in name_project
    ).strip().replace(" ", "_")

    project_folder = f"{id_project}-{safe_name}"

    output_dir = (
        Path(settings.BASE_DIR)
        / "tests_generated"
        / project_folder
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    # Configuration JSON pour K6
    config_json = json.dumps(
        config,
        ensure_ascii=False,
        indent=4
    )

    # Configuration JSON encodée pour Python / Locust
    config_json_python = repr(
        json.dumps(config, ensure_ascii=False)
    )

    # ---------------- K6 ----------------

    k6_content = f'''
import http from 'k6/http';
import {{ check, sleep }} from 'k6';

const CONFIG = {config_json};

export const options = {{
    scenarios: {{
        load_test: {{
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                {{
                    duration: `${{CONFIG.ramp_up}}s`,
                    target: CONFIG.nb_threads
                }},
                {{
                    duration: `${{Math.max(0, CONFIG.duree_secondes - CONFIG.ramp_up)}}s`,
                    target: CONFIG.nb_threads
                }}
            ]
        }}
    }}
}};

function buildUrl(url, params) {{

    const query = Object.entries(params || {{}})
        .map(([key, value]) =>
            encodeURIComponent(key) + '=' + encodeURIComponent(value)
        )
        .join('&');

    if (!query) return url;

    return url + (url.includes('?') ? '&' : '?') + query;
}}

export default function () {{

    const url = buildUrl(
        CONFIG.url_endpoint,
        CONFIG.params_url
    );

    const headers = CONFIG.headers || {{}};

    const options = {{
        headers: headers
    }};

    const method = CONFIG.method.toUpperCase();

    let response;

    switch (method) {{

        case 'GET':
            response = http.get(url, options);
            break;

        case 'POST':
            response = http.post(
                url,
                JSON.stringify(CONFIG.body || {{}}),
                options
            );
            break;

        case 'PUT':
            response = http.put(
                url,
                JSON.stringify(CONFIG.body || {{}}),
                options
            );
            break;

        case 'PATCH':
            response = http.patch(
                url,
                JSON.stringify(CONFIG.body || {{}}),
                options
            );
            break;

        case 'DELETE':
            response = http.del(url, null, options);
            break;

        default:
            throw new Error('Méthode HTTP non supportée');
    }}

    check(response, {{
        'HTTP status 200': r => r.status >= 200 && r.status < 300
    }});

    sleep(CONFIG.think_time);
}}
'''

    # ---------------- LOCUST ----------------

    locust_content = f'''
import json

from locust import HttpUser, task, constant

CONFIG = json.loads({config_json_python})


class PerformanceUser(HttpUser):

    wait_time = constant(CONFIG["think_time"])

    @task
    def execute_request(self):

        method = CONFIG["method"].upper()

        url = CONFIG["url_endpoint"]

        headers = CONFIG.get("headers") or {{}}

        params = CONFIG.get("params_url") or {{}}

        body = CONFIG.get("body") or {{}}

        if method == "GET":

            self.client.get(
                url,
                headers=headers,
                params=params
            )

        elif method == "POST":

            self.client.post(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "PUT":

            self.client.put(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "PATCH":

            self.client.patch(
                url,
                json=body,
                headers=headers,
                params=params
            )

        elif method == "DELETE":

            self.client.delete(
                url,
                headers=headers,
                params=params
            )
'''

    # Création des fichiers
    k6_path = output_dir / f"k6-{id_scenario}.js"

    locust_path = output_dir / f"locust-{id_scenario}.py"

    k6_path.write_text(k6_content, encoding="utf-8")

    locust_path.write_text(locust_content, encoding="utf-8")

    return str(k6_path), str(locust_path)




def insert_scenario(data, user_id):

    with transaction.atomic():

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT name_pr
                FROM projects
                WHERE id_project = %s
            """, [data["id_project"]])

            project = cursor.fetchone()

            if not project:
                raise ValueError("Projet introuvable.")

            name_project = project[0]

            # Préparation des valeurs JSON
            seuils = data.get("seuils_performance")

            seuils_json = (
                json.dumps(seuils)
                if seuils is not None else None
            )

            headers_json = json.dumps(
                data.get("headers") or {}
            )

            params_json = json.dumps(
                data.get("params_url") or {}
            )

            body = data.get("body")

            body_json = (
                json.dumps(body)
                if body is not None else None
            )

            # Appel de la procédure PostgreSQL
            cursor.execute("""
                CALL sp_insert_scenario_v2(
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s::jsonb,
                    %s, %s::jsonb, %s::jsonb, %s::jsonb,
                    %s,
                    NULL
                )
            """, [

                data["name_scenario"],
                data.get("description"),
                data.get("objectif"),

                data["id_project"],
                user_id,
                data["id_type_test"],

                data["id_envir"],
                data["id_outilt"],
                data["id_protocol"],

                data["duree_secondes"],
                data["nb_threads"],
                data.get("ramp_up", 0),
                data.get("think_time", 0),

                data.get("nb_threads_initial"),
                data.get("nb_threads_max"),
                data.get("step_threads"),
                data.get("step_duration_seconds"),

                data.get("volume_donnees"),
                seuils_json,

                data["url_endpoint"],
                headers_json,
                params_json,
                body_json,

                data.get("nb_repetitions", 1)
            ])

            result = cursor.fetchone()

            if not result:
                raise ValueError(
                    "La procédure n'a retourné aucun identifiant."
                )

            id_scenario = result[0]

        # Configuration des moteurs
        config = {
            "method": data["method"],
            "url_endpoint": data["url_endpoint"],
            "headers": data.get("headers") or {},
            "params_url": data.get("params_url") or {},
            "body": data.get("body") or {},
            "nb_threads": int(data["nb_threads"]),
            "duree_secondes": int(data["duree_secondes"]),
            "ramp_up": int(data.get("ramp_up") or 0),
            "think_time": int(data.get("think_time") or 0),
            "nb_repetitions": int(
                data.get("nb_repetitions") or 1
            )
        }

        # Génération des scripts
        k6_path, locust_path = generate_scripts(
            config,
            id_scenario,
            data["id_project"],
            name_project
        )

        return {
            "id_scenario": id_scenario,
            "k6_path": k6_path,
            "locust_path": locust_path
        }
