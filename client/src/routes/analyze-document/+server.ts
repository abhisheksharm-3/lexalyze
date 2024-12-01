import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    try {
        console.log('Received request to analyze document');
        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
            console.error('No file provided in the request');
            return new Response(JSON.stringify({ error: 'File is required' }), { status: 400 });
        }

        console.log('File received:', file.name);

        const apiResponse = await fetch(`${import.meta.env.VITE_SERVER_URI}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!apiResponse.ok) {
            console.error('Failed to analyze document:', apiResponse.statusText);
            return new Response(JSON.stringify({ error: 'Failed to analyze document' }), { status: apiResponse.status });
        }

        const responseData = await apiResponse.json();
        console.log('Document analyzed successfully:', responseData);

        return new Response(JSON.stringify(responseData), { status: 200 });
    } catch (error) {
        console.error('Internal Server Error:', error);
        return new Response(JSON.stringify({ error: 'Internal Server Error' }), { status: 500 });
    }
};
