import { FILE_CONFIG } from './constants';

export const validateFile = (file: File): { isValid: boolean; error?: string } => {
  if (!FILE_CONFIG.validTypes.includes(file.type)) {
    return {
      isValid: false,
      error: "Please upload a PDF, DOC, DOCX, or TXT file"
    };
  }
  
  if (file.size > FILE_CONFIG.maxSize) {
    return {
      isValid: false,
      error: "File size must be less than 10MB"
    };
  }

  return { isValid: true };
};

export const formatFileSize = (bytes: number): string => {
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
};