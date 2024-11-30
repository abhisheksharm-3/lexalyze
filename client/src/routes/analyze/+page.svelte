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
  import { enhance } from "$app/forms";
  import type { ActionData } from "./$types";

  export let form: ActionData;

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
  let progress = tweened(0, { duration: 200 });

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

  const handleDrag = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragActive = e.type === "dragenter" || e.type === "dragover";
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragActive = false;
    error = "";

    if (e.dataTransfer?.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (validateFile(droppedFile)) {
        file = droppedFile;
        analyzing = true;
        simulateAnalysis();
      }
    }
  };

  const handleFileUpload = (e: Event) => {
    error = "";
    const input = e.target as HTMLInputElement;
    if (input.files?.[0]) {
      const selectedFile = input.files[0];
      if (validateFile(selectedFile)) {
        file = selectedFile;
        analyzing = true;
        simulateAnalysis();
      }
    }
  };

  const removeFile = () => {
    file = null;
    progress.set(0);
    analyzing = false;
    error = "";
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
  };

  $: processedData = form?.processedData;
  $: analysisError = form?.error;
</script>

<form method="POST" use:enhance action="?/uploadDocument" enctype="multipart/form-data" class="relative w-full min-h-screen bg-background text-foreground overflow-hidden">
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
                name="file"
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
                    name="question"
                    bind:value={question}
                    placeholder="Ask a question about your document..."
                    class="w-full p-4 pr-12 rounded-lg border border-primary/20 bg-background focus:border-primary focus:ring-1 focus:ring-primary"
                    disabled={!file || analyzing}
                  />
                  <Search
                    class="absolute right-4 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5"
                  />
                </div>

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

              {#if analysisError}
                <div transition:fade>
                  <Alert variant="destructive" class="mt-4">
                    <AlertDescription>{analysisError}</AlertDescription>
                  </Alert>
                </div>
              {/if}

              {#if processedData}
                <div class="mt-4 p-4 bg-primary/5 rounded-lg">
                  <h3 class="font-medium mb-2">Analysis Results:</h3>
                  <p>{processedData}</p>
                </div>
              {/if}

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

              {#if file}
                <div class="border-t border-border pt-6" transition:fade>
                  <div class="flex justify-between items-center mb-4">
                    <span class="font-medium">Export Results</span>
                    <Badge
                      variant="outline"class="text-green-500 bg-green-500/10"
                      >
                        Ready
                      </Badge>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                      {#each ["PDF Report", "Word Document", "JSON Data", "Plain Text"] as format}
                        <Button variant="outline" class="justify-start" type="submit" name="export" value={format}>
                          <Download class="h-4 w-4 mr-2" />
                          {format}
                        </Button>
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
  </form>