<script lang="ts">
  import { FileText, MessageSquare, ArrowRight, Sparkles, Check } from 'lucide-svelte';
  import * as Card from "$lib/components/ui/card";
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import { Alert, AlertDescription } from "$lib/components/ui/alert";

  let email = '';
  let submitted = false;
  let hoveredIndex: number | null = null;

  const features = [
    {
      icon: FileText,
      title: "Smart Analysis",
      description: "Transform complex legal documents into clear, actionable insights using advanced NLP technology",
      iconColor: "text-blue-400"
    },
    {
      icon: MessageSquare,
      title: "AI Assistant",
      description: "Get instant answers to your legal questions with our intelligent chat interface",
      iconColor: "text-violet-400"
    },
    {
      icon: ArrowRight,
      title: "Streamlined Workflow",
      description: "Modern tech stack ensuring lightning-fast processing and seamless integration",
      iconColor: "text-indigo-400"
    }
  ];

  const handleSubmit = () => {
    submitted = true;
    // Add email submission logic here
  };
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 text-white font-inter">
  <!-- Hero Section -->
  <div class="relative overflow-hidden">
    <!-- Background Gradient Orbs -->
    <div class="absolute top-0 -left-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob" />
    <div class="absolute top-0 -right-4 w-72 h-72 bg-violet-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000" />
    <div class="absolute -bottom-8 left-20 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000" />

    <div class="relative container mx-auto px-4 py-16 flex flex-col items-center justify-center space-y-8">
      <!-- Logo/Name Section -->
      <div class="relative group cursor-pointer">
        <h1 class="font-cal text-6xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-violet-400 to-indigo-400 pb-2 transition-all duration-300 hover:scale-105">
          Lexalyze
        </h1>
        <div class="absolute -top-6 -right-6">
          <Sparkles class="w-8 h-8 text-blue-400 animate-pulse" />
        </div>
      </div>

      <!-- Tagline -->
      <p class="font-outfit text-xl md:text-2xl text-slate-300 max-w-2xl text-center leading-relaxed">
        Transforming legal documents into intelligent insights with the power of AI
      </p>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 w-full max-w-6xl">
        {#each features as feature, index}
          <Card.Root 
            class="bg-slate-800/50 border-slate-700 transition-all duration-300 transform {hoveredIndex === index ? 'scale-105 border-blue-500/30' : ''}"
            on:mouseenter={() => hoveredIndex = index}
            on:mouseleave={() => hoveredIndex = null}
          >
            <Card.Content class="p-6">
              <svelte:component 
                this={feature.icon} 
                class="w-8 h-8 {feature.iconColor} mb-3 transition-transform duration-300 {hoveredIndex === index ? 'scale-110' : ''}" 
              />
              <h3 class="font-outfit text-lg font-semibold mb-2">{feature.title}</h3>
              <p class="font-inter text-slate-400 text-sm leading-relaxed">{feature.description}</p>
            </Card.Content>
          </Card.Root>
        {/each}
      </div>

      <!-- Email Signup Section -->
      <div class="mt-16 w-full max-w-md">
        {#if submitted}
          <Alert class="bg-green-500/20 border-green-500/50 text-green-400">
            <Check class="w-4 h-4" />
            <AlertDescription>
              Thanks for signing up! We'll notify you when we launch.
            </AlertDescription>
          </Alert>
        {:else}
          <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div class="flex flex-col md:flex-row gap-4">
              <Input
                type="email"
                bind:value={email}
                placeholder="Enter your email"
                class="flex-1 bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-400 focus:border-blue-500 transition-colors"
                required
              />
              <Button 
                type="submit"
                class="bg-blue-500 hover:bg-blue-600 transition-colors duration-300"
              >
                Notify Me
              </Button>
            </div>
            <p class="text-sm text-slate-400 text-center">
              Be the first to know when we launch
            </p>
          </form>
        {/if}
      </div>

      <!-- Footer -->
      <div class="mt-16 text-sm text-slate-400">
        © 2024 Lexalyze. All rights reserved.
      </div>
    </div>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  @keyframes blob {
    0% {
      transform: translate(0px, 0px) scale(1);
    }
    33% {
      transform: translate(30px, -50px) scale(1.1);
    }
    66% {
      transform: translate(-20px, 20px) scale(0.9);
    }
    100% {
      transform: translate(0px, 0px) scale(1);
    }
  }

  .animate-blob {
    animation: blob 7s infinite;
  }

  .animation-delay-2000 {
    animation-delay: 2s;
  }

  .animation-delay-4000 {
    animation-delay: 4s;
  }

</style>