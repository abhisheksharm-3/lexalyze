import type { ComponentType } from "svelte";

export interface AnalysisFeature {
    icon: any; // Using any here since we're importing from lucide-svelte
    text: string;
    description: string;
  }
  
  export interface FileValidationResult {
    isValid: boolean;
    error?: string;
  }

  export interface Feature {
    icon: ComponentType;
    text: string;
    description: string;
  }