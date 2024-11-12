<script lang="ts">
  import { 
    ConstructionIcon,
    ArrowRightIcon,
    ClockIcon,
    BrainCircuitIcon,
    WorkflowIcon,
    PenToolIcon,
    ChevronRightIcon
  } from 'lucide-svelte';
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { fade, fly } from 'svelte/transition';
  import Progress from '../ui/progress/progress.svelte';
  
  export let pageTitle = "This Section";
  export let estimatedTime = "Coming Soon";
  
  const features = [
    {
      icon: BrainCircuitIcon,
      text: "In Development",
      description: "Our team is hard at work",
      delay: 0
    },
    {
      icon: WorkflowIcon,
      text: "New Features",
      description: "Exciting capabilities ahead",
      delay: 100
    },
    {
      icon: PenToolIcon,
      text: "Final Touches",
      description: "Polishing the experience",
      delay: 200
    },
    {
      icon: ClockIcon,
      text: "Stay Tuned",
      description: "Worth the wait",
      delay: 300
    }
  ];

  let isHovered = false;
</script>

<div class="relative w-full bg-background text-foreground overflow-hidden min-h-screen flex items-center">
  <!-- Enhanced gradient background with animation -->
  <div class="absolute inset-0">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(var(--primary-rgb),0.08),transparent_60%)] animate-pulse"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_bottom_right,rgba(var(--primary-rgb),0.05),transparent_50%)]"></div>
  </div>
  
  <div class="container relative mx-auto px-4 py-32 sm:px-6 lg:px-8">
    <div class="grid gap-20 lg:grid-cols-2 items-center">
      <!-- Left Column - Enhanced Content -->
      <div class="relative z-10 flex flex-col justify-center space-y-14">
        <!-- Animated Status Badge -->
        <div in:fly="{{ y: 20, duration: 800, delay: 200 }}">
          <Badge variant="outline" class="w-fit bg-background/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow duration-300">
            <ConstructionIcon class="mr-1.5 h-3.5 w-3.5" />
            {estimatedTime}
          </Badge>
        </div>

        <!-- Main Content with enhanced animations -->
        <div class="space-y-8" in:fly="{{ y: 30, duration: 1000, delay: 400 }}">
          <h1 class="font-serif text-5xl font-bold tracking-tight sm:text-6xl xl:text-7xl">
            <span class="block text-muted-foreground/90 hover:text-muted-foreground transition-colors duration-300">
              {pageTitle} is
            </span>
            <span class="relative mt-3 block text-primary">
              Under Construction
              <svg class="absolute -bottom-2 left-0 h-2.5 w-full fill-none stroke-primary stroke-[4] animate-pulse" viewBox="0 0 100 10">
                <path d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5" vector-effect="non-scaling-stroke"/>
              </svg>
            </span>
          </h1>
          
          <p class="max-w-xl text-xl leading-relaxed text-muted-foreground/90 hover:text-muted-foreground transition-colors duration-300">
            We're working on something amazing for this section. Check back soon to see what we're building.
          </p>
        </div>

        <!-- Enhanced CTA Button -->
        <div in:fly="{{ y: 40, duration: 1200, delay: 600 }}">
          <Button 
            size="lg" 
            variant="outline" 
            class="group relative px-8 py-6 hover:shadow-lg transition-all duration-300"
            on:click={() => history.back()}
            on:mouseenter={() => isHovered = true}
            on:mouseleave={() => isHovered = false}
          >
            <span class="relative z-10 flex items-center text-lg font-medium">
              Go Back
              <ChevronRightIcon class="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1.5" />
            </span>
            {#if isHovered}
              <div 
                class="absolute inset-0 bg-primary/5 rounded-md" 
                in:fade="{{ duration: 200 }}"
              ></div>
            {/if}
          </Button>
        </div>
      </div>

      <!-- Right Column - Enhanced Status Card -->
      <div class="relative" in:fly="{{ x: 30, duration: 1000, delay: 800 }}">
        <!-- Animated Background Cards -->
        <Card class="absolute -right-4 -top-4 h-full w-full bg-primary/5 transition-transform hover:scale-[1.02] duration-500"></Card>
        <Card class="absolute -right-8 -top-8 h-full w-full bg-primary/5 transition-transform hover:scale-[1.01] duration-500"></Card>

        <!-- Main Content Card -->
        <Card class="relative z-10 overflow-hidden backdrop-blur-sm border-primary/10 hover:border-primary/20 transition-colors duration-300">
          <!-- Enhanced Card Header -->
          <div class="border-b border-border/50 p-7">
            <div class="flex items-center justify-between">
              <Badge variant="outline" class="bg-primary/5 px-4 py-1.5 hover:bg-primary/10 transition-colors duration-300">
                <span class="relative flex h-2 w-2">
                  <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75"></span>
                  <span class="relative inline-flex h-2 w-2 rounded-full bg-primary"></span>
                </span>
                <span class="ml-2 font-medium">In Progress</span>
              </Badge>
            </div>
          </div>

          <!-- Enhanced Card Content -->
          <div class="space-y-10 p-7">
            <!-- Animated Progress Indicator -->
            <div class="space-y-4">
              <div class="flex justify-between">
                <span class="text-sm font-medium">Development Progress</span>
                <span class="text-sm text-muted-foreground">75%</span>
              </div>
              <Progress value={75} class="h-2" />
            </div>

            <!-- Enhanced Feature Grid -->
            <div class="grid grid-cols-2 gap-8">
              {#each features as feature}
                <div 
                  class="group space-y-3 hover:translate-y-[-2px] transition-all duration-300"
                  in:fly="{{ y: 20, duration: 800, delay: feature.delay }}"
                >
                  <div class="flex items-center gap-3">
                    <div class="rounded-lg bg-primary/10 p-2.5 transition-colors group-hover:bg-primary/20 group-hover:scale-105 duration-300">
                      <svelte:component this={feature.icon} class="h-5 w-5 text-primary group-hover:animate-bounce" />
                    </div>
                    <span class="font-medium group-hover:text-primary transition-colors duration-300">{feature.text}</span>
                  </div>
                  <p class="text-sm text-muted-foreground group-hover:text-muted-foreground/80 transition-colors duration-300">
                    {feature.description}
                  </p>
                </div>
              {/each}
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</div>

<style>
  @keyframes spin-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  :global(.animate-spin-slow) {
    animation: spin-slow 3s linear infinite;
  }
</style>