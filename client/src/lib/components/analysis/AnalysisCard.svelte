<script lang="ts">
    import { Search, FileQuestion, Clock, Download } from "lucide-svelte";
    import { Badge } from "$lib/components/ui/badge";
    import { Button } from "$lib/components/ui/button";
    import { Card } from "$lib/components/ui/card";
    import { fade } from "svelte/transition";
    import { FEATURES, SUGGESTED_QUESTIONS, EXPORT_FORMATS } from '../../constants';
  
    export let file: File | null = null;
    export let analyzing = false;
    export let progress = 0;
    export let question = "";
  
    const setQuestionFromSuggestion = (q: string) => {
      question = q;
    };
  </script>
  
  <div class="relative h-full">
    <div class="relative w-full h-full min-h-[600px]">
      <!-- Background Cards -->
      <div class="absolute inset-0 transform">
        <Card class="absolute inset-0 translate-x-4 translate-y-4 bg-primary/5" />
        <Card class="absolute inset-0 translate-x-8 translate-y-8 bg-primary/5" />
      </div>
  
      <!-- Main Card -->
      <Card class="relative h-full backdrop-blur-sm">
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
                <span class="text-sm text-muted-foreground">{progress}%</span>
              </div>
              <div class="h-2 rounded-full bg-primary/20">
                <div
                  class="h-full rounded-full bg-primary transition-all duration-300"
                  style="width: {progress}%"
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
  
            <div class="grid grid-cols-2 gap-3">
              {#each SUGGESTED_QUESTIONS as q}
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
            {#each FEATURES as feature}
              <div class="group space-y-2">
                <div class="flex items-center gap-3">
                  <div
                    class="rounded-lg bg-primary/10 p-2 transition-colors group-hover:bg-primary/20"
                  >
                    <svelte:component this={feature.icon} class="h-5 w-5 text-primary" />
                  </div>
                  <span class="font-medium">{feature.text}</span>
                </div>
                <p class="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            {/each}
          </div>
  
          {#if progress === 100}
            <div class="border-t border-border pt-6" transition:fade>
              <div class="flex justify-between items-center mb-4">
                <span class="font-medium">Export Results</span>
                <Badge variant="outline" class="text-green-500 bg-green-500/10">
                  Ready
                </Badge>
              </div>
              <div class="grid grid-cols-2 gap-3">
                {#each EXPORT_FORMATS as format}
                  <Button variant="outline" class="justify-start">
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