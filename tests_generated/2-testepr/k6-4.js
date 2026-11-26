
import http from 'k6/http';
import { check, sleep } from 'k6';

const CONFIG = {
    "method": "POST",
    "url_endpoint": "http://sdfsdf.md",
    "headers": {},
    "params_url": {},
    "body": {},
    "nb_threads": 30,
    "duree_secondes": 600,
    "ramp_up": 60,
    "think_time": 0,
    "nb_repetitions": 1
};

export const options = {
    scenarios: {
        load_test: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                {
                    duration: `${CONFIG.ramp_up}s`,
                    target: CONFIG.nb_threads
                },
                {
                    duration: `${Math.max(0, CONFIG.duree_secondes - CONFIG.ramp_up)}s`,
                    target: CONFIG.nb_threads
                }
            ]
        }
    }
};

function buildUrl(url, params) {

    const query = Object.entries(params || {})
        .map(([key, value]) =>
            encodeURIComponent(key) + '=' + encodeURIComponent(value)
        )
        .join('&');

    if (!query) return url;

    return url + (url.includes('?') ? '&' : '?') + query;
}

export default function () {

    const url = buildUrl(
        CONFIG.url_endpoint,
        CONFIG.params_url
    );

    const headers = CONFIG.headers || {};

    const options = {
        headers: headers
    };

    const method = CONFIG.method.toUpperCase();

    let response;

    switch (method) {

        case 'GET':
            response = http.get(url, options);
            break;

        case 'POST':
            response = http.post(
                url,
                JSON.stringify(CONFIG.body || {}),
                options
            );
            break;

        case 'PUT':
            response = http.put(
                url,
                JSON.stringify(CONFIG.body || {}),
                options
            );
            break;

        case 'PATCH':
            response = http.patch(
                url,
                JSON.stringify(CONFIG.body || {}),
                options
            );
            break;

        case 'DELETE':
            response = http.del(url, null, options);
            break;

        default:
            throw new Error('Méthode HTTP non supportée');
    }

    check(response, {
        'HTTP status 200': r => r.status >= 200 && r.status < 300
    });

    sleep(CONFIG.think_time);
}
