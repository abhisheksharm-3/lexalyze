<script lang="ts">
    import { Upload, FileText, X } from "lucide-svelte";
    import { Button } from "$lib/components/ui/button";
    import { Card } from "$lib/components/ui/card";
    import { Alert, AlertDescription } from "$lib/components/ui/alert";
    import { fade } from "svelte/transition";
    import { validateFile, formatFileSize } from '../../fileUtils';
    
    export let file: File | null = null;
    export let analyzing = false;
    export let dragActive = false;
    export let error = "";
  
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
        const validation = validateFile(droppedFile);
        if (validation.isValid) {
          file = droppedFile;
          analyzing = true;
          dispatch('startAnalysis');
        } else {
          error = validation.error || "Invalid file";
        }
      }
    };
  
    const handleFileUpload = (e: Event) => {
      error = "";
      const input = e.target as HTMLInputElement;
      if (input.files?.[0]) {
        const selectedFile = input.files[0];
        const validation = validateFile(selectedFile);
        if (validation.isValid) {
          file = selectedFile;
          analyzing = true;
          dispatch('startAnalysis');
        } else {
          error = validation.error || "Invalid file";
        }
      }
    };
  
    const removeFile = () => {
      file = null;
      dispatch('removeFile');
    };
  
    function dispatch(name: string) {
      const event = new CustomEvent(name);
      dispatchEvent(event);
    }
  </script>
  
  <Card class="relative overflow-hidden backdrop-blur-sm border-primary/10 transition-colors duration-300">
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
                  {formatFileSize(file.size)}
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