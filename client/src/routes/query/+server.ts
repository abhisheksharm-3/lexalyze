import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    try {
        console.log('Received POST request');
        const { question, doc_id, context } = await request.json();
        console.log('Request payload:', { question, doc_id, context });

        const response = await fetch(`${import.meta.env.VITE_SERVER_URI}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                doc_id, 
                question, 
                context: JSON.stringify(context) 
            })
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

        return new Response(JSON.stringify(data), {
            status: response.status,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error('Error fetching data from API:', error);
        return new Response(JSON.stringify({ error: 'Failed to fetch data from API' }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
};