<script lang="ts">
  import {
    FileText,
    Upload,
    MessageSquare,
    Search,
    BarChart2,
    FileQuestion,
    CheckCircle2,
    ArrowRight,
    Clock,
    Download,
    X,
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Alert, AlertDescription } from "$lib/components/ui/alert";
  import { tweened } from "svelte/motion";
  import { fade } from "svelte/transition";
  import { Dialog } from "$lib/components/ui/dialog";
  import DialogContent from "$lib/components/ui/dialog/dialog-content.svelte";
  import DialogHeader from "$lib/components/ui/dialog/dialog-header.svelte";
  import DialogTitle from "$lib/components/ui/dialog/dialog-title.svelte";
  import DialogDescription from "$lib/components/ui/dialog/dialog-description.svelte";
  import jsPDF from 'jspdf';
  import mammoth from 'mammoth';
  import FileSaver from 'file-saver';
const { saveAs } = FileSaver;

  interface AnalysisFeature {
    icon: typeof FileText;
    text: string;
    description: string;
  }

  let isCardHovered = false;
  let file: File | null = null;
  let analyzing = false;
  let dragActive = false;
  let error = "";
  let question = "";
  let responseData: any = null;
  let doc_id: string | null = null;
  let progress = tweened(0, { duration: 200 });
  let queryAnswer = "";
  let isDialogOpen = false;

  const features: AnalysisFeature[] = [
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

  const trustIndicators = [
    "AI-Powered Analysis",
    "Real-time Processing",
    "Secure Storage",
    "Export Ready",
  ];

  const suggestedQuestions = [
    "What are the main topics?",
    "Summarize key findings",
    "List requirements",
    "Technical specifications",
  ];

  const validateFile = (file: File): boolean => {
    const validTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "text/plain",
    ];
    if (!validTypes.includes(file.type)) {
      error = "Please upload a PDF, DOC, DOCX, or TXT file";
      return false;
    }
    if (file.size > 10 * 1024 * 1024) {
      error = "File size must be less than 10MB";
      return false;
    }
    return true;
  };
  const exportPDF = () => {
  if (!responseData) return;

  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });
  
  // Set up some variables for positioning
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 10;
  
  // Title
  doc.setFontSize(18);
  doc.text('Document Analysis Report', margin, 20);
  
  // File details
  doc.setFontSize(12);
  doc.text(`File: ${file?.name || 'Unknown'}`, margin, 30);
  doc.text(`Analyzed on: ${new Date().toLocaleString()}`, margin, 37);

  // Analysis Result
  doc.setFontSize(14);
  doc.text('Analysis Result:', margin, 50);
  
  // Convert responseData to a formatted string
  const analysisText = JSON.stringify(responseData, null, 2);
  
  // Split text with a larger width to accommodate more characters per line
  const splitText = doc.splitTextToSize(analysisText, pageWidth - 2 * margin);
  
  // Add text with auto page breaking
  doc.setFontSize(10);
  doc.text(splitText, margin, 60, {
    maxWidth: pageWidth - 2 * margin,
    align: 'left'
  });

  // Save the PDF
  doc.save('document_analysis_report.pdf');
};

const exportWord = () => {
  if (!responseData) return;

  // Create a simple HTML content for Word export
  const content = `
    <html>
      <head>
        <meta charset="utf-8">
        <title>Document Analysis Report</title>
      </head>
      <body>
        <h1>Document Analysis Report</h1>
        <p><strong>File:</strong> ${file?.name || 'Unknown'}</p>
        <p><strong>Analyzed on:</strong> ${new Date().toLocaleString()}</p>
        
        <h2>Analysis Result</h2>
        <pre>${JSON.stringify(responseData, null, 2)}</pre>
      </body>
    </html>
  `;

  // Convert HTML to Word document blob
  const blob = new Blob([content], { 
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
  });
  saveAs(blob, 'document_analysis_report.docx');
};

const exportJSON = () => {
  if (!responseData) return;

  const exportData = {
    fileName: file?.name,
    analyzedAt: new Date().toISOString(),
    analysisResult: responseData
  };

  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
  saveAs(blob, 'document_analysis_report.json');
};

const exportPlainText = () => {
  if (!responseData) return;

  const content = `Document Analysis Report

File: ${file?.name || 'Unknown'}
Analyzed on: ${new Date().toLocaleString()}

Analysis Result:
${JSON.stringify(responseData, null, 2)}
  `;

  const blob = new Blob([content], { type: 'text/plain' });
  saveAs(blob, 'document_analysis_report.txt');
};
const handleDrag = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragActive = e.type === "dragenter" || e.type === "dragover";
  };
  const handleDrop = async (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
    error = "";

    if (e.dataTransfer?.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (validateFile(droppedFile)) {
        file = droppedFile;
        await analyzeDocument();
      }
    }
  };

  const handleFileUpload = async (e: Event) => {
    error = "";
    const input = e.target as HTMLInputElement;
    if (input.files?.[0]) {
      const selectedFile = input.files[0];
      if (validateFile(selectedFile)) {
        file = selectedFile;
        await analyzeDocument();
      }
    }
  };

  const removeFile = () => {
    file = null;
    progress.set(0);
    analyzing = false;
    error = "";
    doc_id = null;
    responseData = null;
  };

  const analyzeDocument = async () => {
    if (!file) return;
    analyzing = true;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/analyze-document", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        doc_id = data.doc_id;
        responseData = data;
        simulateAnalysis();
      } else {
        throw new Error(data.error || "Failed to analyze document");
      }
    } catch (err) {
      error = (err as Error).message || "An error occurred";
      analyzing = false;
    }
  };

  const sendQuery = async () => {
    if (!doc_id || !question.trim()) {
      error = "Document ID or question is missing.";
      return;
    }

    try {
      analyzing = true;

      const response = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          doc_id,
          question: question.trim(),
          context: responseData,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Query failed.");
      }

      const data = await response.json();
      queryAnswer = data.answer;
      isDialogOpen = true;
    } catch (err) {
      error = err instanceof Error ? err.message : "An error occurred";
    } finally {
      analyzing = false;
    }
  };


  const simulateAnalysis = () => {
    let currentProgress = 0;
    const interval = setInterval(() => {
      if (currentProgress >= 100) {
        clearInterval(interval);
        analyzing = false;
      } else {
        currentProgress += 2;
        progress.set(currentProgress);
      }
    }, 100);
  };

  const setQuestionFromSuggestion = (q: string) => {
    question = q;
    sendQuery();
  };
</script>


<div
  class="relative w-full min-h-screen bg-background text-foreground overflow-hidden"
>
  <div class="absolute inset-0">
    <div
      class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(var(--primary-rgb),0.04),transparent_50%)]"
    ></div>
  </div>

  <div class="container relative mx-auto px-4 py-12 sm:px-6 lg:px-8 flex items-center min-h-screen">
    <div class="grid gap-8 lg:grid-cols-2">
      <!-- Left Column -->
      <div class="relative z-10 flex flex-col justify-center space-y-8">
        <div class="flex flex-wrap gap-2">
          {#each trustIndicators as indicator}
            <Badge variant="outline" class="bg-background/80 backdrop-blur-sm">
              <CheckCircle2 class="mr-1.5 h-3.5 w-3.5" />
              {indicator}
            </Badge>
          {/each}
        </div>

        <div class="space-y-6">
          <h1
            class="font-serif text-4xl font-bold tracking-tight sm:text-5xl xl:text-6xl"
          >
            <span class="block text-muted-foreground">Document</span>
            <span class="relative mt-2 block text-primary">
              Analysis
              <svg
                class="absolute -bottom-2 left-0 h-2 w-full fill-none stroke-primary stroke-[4] -translate-x-16"
                viewBox="0 0 100 10"
              >
                <path
                  d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5"
                  vector-effect="non-scaling-stroke"
                />
              </svg>
            </span>
          </h1>

          <p class="max-w-xl text-lg leading-relaxed text-muted-foreground">
            Upload your documents for AI-powered analysis, insights, and
            interactive Q&A.
          </p>
        </div>

        <Card
          class="relative overflow-hidden backdrop-blur-sm border-primary/10 transition-colors duration-300"
        >
          <div class="p-6">
            <div
              role="button"
              tabindex="0"
              class="relative border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-300 {dragActive
                ? 'border-primary bg-primary/5'
                : 'border-primary/20 hover:border-primary/40'}"
              on:dragenter={handleDrag}
              on:dragleave={handleDrag}
              on:dragover={handleDrag}
              on:drop={handleDrop}
            >
              <input
                type="file"
                id="file-upload"
                class="hidden"
                on:change={handleFileUpload}
                accept=".pdf,.doc,.docx,.txt"
              />
              {#if error}
                <div transition:fade>
                  <Alert variant="destructive" class="mb-4">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                </div>
              {/if}
              {#if file}
                <div
                  class="flex items-center justify-between p-4 bg-primary/5 rounded-lg"
                  transition:fade
                >
                  <div class="flex items-center space-x-4">
                    <FileText class="h-8 w-8 text-primary" />
                    <div class="text-left">
                      <p class="font-medium truncate max-w-[200px]">
                        {file.name}
                      </p>
                      <p class="text-sm text-muted-foreground">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    on:click={removeFile}
                    class="hover:text-destructive"
                  >
                    <X class="h-5 w-5" />
                  </Button>
                </div>
              {:else}
                <label
                  for="file-upload"
                  class="cursor-pointer flex flex-col items-center gap-4"
                >
                  <div class="rounded-full bg-primary/10 p-4">
                    <Upload class="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p class="text-lg font-medium">
                      Drop your document here or click to upload
                    </p>
                    <p class="text-sm text-muted-foreground mt-1">
                      Supports PDF, DOC, DOCX, and TXT (max 10MB)
                    </p>
                  </div>
                  <Button variant="outline" class="mt-2">Select File</Button>
                </label>
              {/if}
            </div>
          </div>
        </Card>
      </div>

      <!-- Right Column -->
      <div class="relative h-full">
        <div class="relative w-full h-full min-h-[600px]">
          <!-- Background Cards -->
          <div class="absolute inset-0 transform">
            <Card
              class="absolute inset-0 translate-x-4 translate-y-4 bg-primary/5"
            />
            <Card
              class="absolute inset-0 translate-x-8 translate-y-8 bg-primary/5"
            />
          </div>

          <!-- Main Card -->
          <Card
            class="relative h-full backdrop-blur-sm"
            on:mouseenter={() => (isCardHovered = true)}
            on:mouseleave={() => (isCardHovered = false)}
          >
            <div class="border-b border-border p-6">
              <div class="flex items-center justify-between">
                <Badge variant="outline" class="bg-primary/5 px-4 py-1.5">
                  <span class="relative flex h-2 w-2">
                    <span
                      class="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75"
                    ></span>
                    <span
                      class="relative inline-flex h-2 w-2 rounded-full bg-primary"
                    ></span>
                  </span>
                  <span class="ml-2 font-medium">
                    {analyzing
                      ? "Processing..."
                      : file
                        ? "Ready"
                        : "Waiting for file"}
                  </span>
                </Badge>
                {#if file}
                  <Badge variant="outline" class="gap-1.5">
                    <Clock class="h-3.5 w-3.5" />
                    Real-time
                  </Badge>
                {/if}
              </div>
            </div>

            <div class="space-y-6 p-6">
              {#if analyzing}
                <div class="space-y-3" transition:fade>
                  <div class="flex justify-between">
                    <span class="text-sm font-medium">Analyzing Document</span>
                    <span class="text-sm text-muted-foreground"
                      >{$progress}%</span
                    >
                  </div>
                  <div class="h-2 rounded-full bg-primary/20">
                    <div
                      class="h-full rounded-full bg-primary transition-all duration-300"
                      style="width: {$progress}%"
                    ></div>
                  </div>
                </div>
              {/if}

              <div class="space-y-4">
                <div class="relative">
                  <input
                    type="text"
                    bind:value={question}
                    placeholder="Ask a question about your document..."
                    class="w-full p-4 pr-12 rounded-lg border border-primary/20 bg-background focus:border-primary focus:ring-1 focus:ring-primary"
                    disabled={!file || analyzing}
                  />
                  <Search
                    class="absolute right-4 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5"
                  />
                </div>
                <button 
                  class="focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 shadow h-9 px-4 py-2 w-full mt-2"
                  disabled={!file || analyzing || !question.trim()}
                  on:click={sendQuery}
                >
                  <MessageSquare class="h-4 w-4 mr-2" />
                  Submit Query
                  <ArrowRight class="h-4 w-4 ml-2" />
                </button>

                <div class="grid grid-cols-2 gap-3">
                  {#each suggestedQuestions as q}
                    <Button
                      variant="outline"
                      class="text-sm justify-start"
                      disabled={!file || analyzing}
                      on:click={() => setQuestionFromSuggestion(q)}
                    >
                      <FileQuestion class="h-4 w-4 mr-2" />
                      {q}
                    </Button>
                  {/each}
                </div>
              </div>

              <div class="grid grid-cols-2 gap-6">
                {#each features as feature}
                  <div class="group space-y-2">
                    <div class="flex items-center gap-3">
                      <div
                        class="rounded-lg bg-primary/10 p-2 transition-colors group-hover:bg-primary/20"
                      >
                        <svelte:component
                          this={feature.icon}
                          class="h-5 w-5 text-primary"
                        />
                      </div>
                      <span class="font-medium">{feature.text}</span>
                    </div>
                    <p class="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                {/each}
              </div>

              {#if $progress === 100}
                <div class="border-t border-border pt-6" transition:fade>
                  <div class="flex justify-between items-center mb-4">
                    <span class="font-medium">Export Results</span>
                    <Badge
                      variant="outline"
                      class="text-green-500 bg-green-500/10"
                    >
                      Ready
                    </Badge>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    {#each [
                      { format: 'PDF Report', handler: exportPDF },
                      { format: 'Word Document', handler: exportWord },
                      { format: 'JSON Data', handler: exportJSON },
                      { format: 'Plain Text', handler: exportPlainText }
                    ] as { format, handler }}
                      <button 
                        class="focus-visible:ring-ring inline-flex items-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 border-input bg-background hover:bg-accent hover:text-accent-foreground border shadow-sm h-9 px-4 py-2 justify-start"
                        disabled={!$progress || $progress < 100}
                        on:click={handler}
                      >
                        <Download class="h-4 w-4 mr-2" />
                        {format}
                    </button>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
  <Dialog bind:open={isDialogOpen}>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Document Query Result</DialogTitle>
        <DialogDescription>
          {queryAnswer}
        </DialogDescription>
      </DialogHeader>
    </DialogContent>
  </Dialog>
</div>