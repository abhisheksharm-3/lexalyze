import { BarChart2, Clock, FileText, Search } from "lucide-svelte";
import type { Feature } from "./types";

export const FEATURES: Feature[] = [
    {
      icon: FileText,
      text: "Document Review",
      description: "AI-powered content analysis",
    },
    {
      icon: BarChart2,
      text: "Key Insights",
      description: "Extract main concepts",
    },
    {
      icon: Search,
      text: "Smart Search",
      description: "Context-aware queries",
    },
    {
      icon: Clock,
      text: "Processing Time",
      description: "Real-time updates",
    },
  ];

export const TRUST_INDICATORS = [
  "AI-Powered Analysis",
  "Real-time Processing",
  "Secure Storage",
  "Export Ready",
];

export const SUGGESTED_QUESTIONS = [
  "What are the main topics?",
  "Summarize key findings",
  "List requirements",
  "Technical specifications",
];

export const EXPORT_FORMATS = [
  "PDF Report",
  "Word Document",
  "JSON Data",
  "Plain Text",
];

export const FILE_CONFIG = {
  maxSize: 10 * 1024 * 1024, // 10MB
  validTypes: [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
  ],
};