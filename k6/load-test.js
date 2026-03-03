import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 }, // Ramp-up to 50 virtual users over 30s
    { duration: '1m', target: 100 }, // Stay at 100 users for 1 minute
    { duration: '30s', target: 0 },   // Ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'], // 95% of requests must complete below 500ms
    'http_req_failed': ['rate<0.01'],   // Error rate must be less than 1%
  },
};

export default function () {
  const url = 'http://chatbot.example.com/chat/'; // CHANGE THIS TO YOUR SERVICE URL
  const payload = JSON.stringify({
    user_input: 'Tell me a fun fact about space.',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time is less than 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1); // Wait for 1 second between requests
}
