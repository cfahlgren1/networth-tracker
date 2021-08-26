addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request))
})

/**
 * Trigger Airflow Dag using Airflow API
 * @returns Airflow Response
 */
async function startAirflowJob() {
  const endpoint = 'http://airflow.calebfahlgren.com/api/v1/dags/net_worth_notifier/dagRuns'
  const request = {
    body: JSON.stringify({
      conf: {},
      execution_date: new Date().toISOString(), // we want to trigger immediately
    }),
    method: 'POST',
    headers: {
      'Authorization': `Basic ${token}`,
      'Content-Type': 'application/json;',
    },
  }

  const response = await fetch(endpoint, request)
  return response;
}

/**
 * Parse HTTP Basic Authorization value.
 * @param {Request} request
 */
function basicAuthentication(request) {
  const Authorization = request.headers.get('Authorization')
  const [scheme, authToken] = Authorization.split(' ')

  // The Authorization header must start with "Basic", followed by a space.
  if (!authToken || scheme !== 'Basic') {
    return new Response('Malformed authorization header.', {status: 400})
  }
  return authToken
}

/**
 * Respond with Airflow Triggered text
 * @param {Request} request
 */
async function handleRequest(request) {
  if (request.method !== 'POST') {
    return new Response('Please Send a POST request')
  }
  // The "Authorization" header is sent when authenticated.
  if (request.headers.has('Authorization')) {
    const authToken = basicAuthentication(request)

    // check if auth token matches env token
    if (authToken === token) {
      const airflowResponse = await startAirflowJob()
      console.log("POST",airflowResponse.status, airflowResponse.statusText)

      return new Response('Airflow Job Triggered 🚀 !', {
        headers: { 'content-type': 'text/plain' },
      })
    }
  }
  return new Response('Invalid authorization', {status:401})
}
