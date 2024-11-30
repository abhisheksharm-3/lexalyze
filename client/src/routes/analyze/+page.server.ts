import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { z } from 'zod';

// Validation schema for file upload
const FileSchema = z.object({
  name: z.string(),
  type: z.string(),
  size: z.number().max(10 * 1024 * 1024, { message: "File must be less than 10MB" })
});

// Mock AI analysis function (replace with actual AI service)
async function analyzeDocument(file: File, question?: string) {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // In a real-world scenario, this would call an actual AI service
  // For now, we'll return a mock analysis
  return `Analyzed document "${file.name}". Key insights: document contains ${file.type} file type with size ${file.size} bytes. ${question ? `Question asked: ${question}` : 'No specific question provided.'}`;
}

export const load: PageServerLoad = async () => {
  return {};
};

export const actions: Actions = {
  uploadDocument: async ({ request }) => {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    const question = formData.get('question') as string | null;

    // Validate file
    try {
      FileSchema.parse({
        name: file.name,
        type: file.type,
        size: file.size
      });
    } catch (err: unknown) {
      if (err instanceof z.ZodError) {
        return fail(400, { 
          error: err.errors[0].message 
        });
      }
    }

    // Supported file types
    const supportedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ];

    if (!supportedTypes.includes(file.type)) {
      return fail(400, { 
        error: 'Unsupported file type. Please upload PDF, DOC, DOCX, or TXT.' 
      });
    }

    try {
      // Analyze the document
      const processedData = await analyzeDocument(file, question ?? undefined);
      
      return { 
        processedData 
      };
    } catch (error) {
      return fail(500, { 
        error: 'Failed to process document. Please try again.' 
      });
    }
  },

  exportDocument: async ({ request }) => {
    const formData = await request.formData();
    const exportFormat = formData.get('export') as string;

    // In a real-world scenario, you'd generate the export here
    // For now, we'll just simulate an export
    console.log(`Exporting document in ${exportFormat} format`);

    return { 
      exported: true,
      format: exportFormat
    };
  }
};