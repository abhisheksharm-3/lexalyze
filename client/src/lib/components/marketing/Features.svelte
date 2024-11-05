<script lang="ts">
  import { Card, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { 
    Upload,
    Search, 
    MessageSquare,
    Scale,
    BookOpen,
    Shield,
    CheckCircle2,
    ArrowRight
  } from "lucide-svelte";

  const features = [
    {
      icon: Upload,
      title: "Easy Document Upload",
      description: "Securely upload and store your legal documents with just a few clicks.",
      badge: "Enterprise Ready"
    },
    {
      icon: Search,
      title: "Advanced Search",
      description: "Quickly find relevant information across all your documents using AI-powered search.",
      badge: "AI Powered"
    },
    {
      icon: MessageSquare,
      title: "AI Chat Interface",
      description: "Interact with your documents through a natural language chat interface.",
      badge: "Real-time"
    },
    {
      icon: Scale,
      title: "Legal Analysis",
      description: "Get instant insights and analysis of your legal documents, including risk assessment.",
      badge: "99.8% Accurate"
    },
    {
      icon: BookOpen,
      title: "Case Law Integration",
      description: "Automatically link your documents to relevant case law and legal precedents.",
      badge: "Auto-updating"
    },
    {
      icon: Shield,
      title: "Data Security",
      description: "Bank-level encryption and security measures to protect your sensitive legal information.",
      badge: "SOC 2 Type II"
    }
  ];
</script>

<section class="relative w-full overflow-hidden bg-background py-24">
  <!-- Gradient Background -->
  <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom,rgba(var(--primary-rgb),0.04),transparent_50%)]"></div>
  
  <div class="container relative mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Section Header -->
    <div class="mb-16 text-center">
      <h2 class="font-serif text-4xl font-bold tracking-tight sm:text-5xl">
        <span class="block text-muted-foreground">Empowering Legal Teams with</span>
        <span class="relative mt-2 inline-block text-primary">
          Intelligent Tools
          <svg class="absolute -bottom-2 left-0 h-2 w-full fill-none stroke-primary stroke-[4]" viewBox="0 0 100 10">
            <path d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5">
          </svg>
        </span>
      </h2>
      <p class="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
        Advanced features designed specifically for legal professionals, combining AI technology with enterprise-grade security.
      </p>
    </div>

    <!-- Features Grid -->
    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      {#each features as feature, index (index)}
        <Card class="group relative overflow-hidden backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
          <CardHeader>
            <!-- Feature Badge -->
            <Badge variant="outline" class="mb-6 w-fit bg-primary/5">
              <CheckCircle2 class="mr-1.5 h-3.5 w-3.5" />
              {feature.badge}
            </Badge>

            <!-- Icon -->
            <div class="mb-6 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 transition-colors group-hover:bg-primary/20">
              <svelte:component this={feature.icon} class="h-6 w-6 text-primary" />
            </div>

            <!-- Content -->
            <CardTitle class="mb-2 text-xl">
              {feature.title}
            </CardTitle>
            <CardDescription class="text-muted-foreground">
              {feature.description}
            </CardDescription>

            <!-- Hover State Arrow -->
            <div class="mt-4 flex items-center text-sm font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
              Learn more
              <ArrowRight class="ml-1 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </div>
          </CardHeader>
        </Card>
      {/each}
    </div>
  </div>
</section>