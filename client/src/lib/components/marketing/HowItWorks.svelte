<script lang="ts">
  import { Card, CardHeader, CardContent } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Upload, Search, Brain, MessageSquare, ArrowRight, CheckCircle2 } from "lucide-svelte";

  const steps = [
    {
      icon: Upload,
      title: "Upload Documents",
      description: "Securely upload your legal documents to the Lexalyze platform.",
      badge: "Step 1"
    },
    {
      icon: Brain,
      title: "AI Analysis",
      description: "Our advanced AI analyzes your documents, extracting key information and insights.",
      badge: "Step 2"
    },
    {
      icon: Search,
      title: "Explore Insights",
      description: "Review AI-generated summaries, risk assessments, and relevant case law connections.",
      badge: "Step 3"
    },
    {
      icon: MessageSquare,
      title: "Chat and Inquire",
      description: "Ask questions about your documents using our AI-powered chat interface.",
      badge: "Step 4"
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
        <span class="block text-muted-foreground">Understanding</span>
        <span class="relative mt-2 inline-block text-primary">
          How Lexalyze Works
          <svg class="absolute -bottom-2 left-0 h-2 w-full fill-none stroke-primary stroke-[4]" viewBox="0 0 100 10">
            <path d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5"/>
          </svg>
        </span>
      </h2>
      <p class="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
        Follow our simple four-step process to transform your legal document workflow with AI-powered insights.
      </p>
    </div>

    <div class="relative">
      <!-- Vertical line -->
      <div class="absolute left-4 inset-y-0 w-0.5 bg-primary/30 md:left-1/2 md:-ml-0.5"></div>

      <div class="space-y-12 relative">
        {#each steps as step, index}
          <div class="flex items-center {index % 2 === 0 ? 'md:flex-row-reverse' : ''} group">
            <div class="flex-1 md:w-1/2"></div>
            
            <!-- Timeline Node -->
            <div 
              class="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground shrink-0 mx-4 md:mx-6 z-10 
              transition-transform duration-300 group-hover:scale-110 group-hover:shadow-lg"
            >
              {index + 1}
            </div>

            <!-- Card -->
            <Card 
              class="flex-1 md:w-1/2 group relative overflow-hidden backdrop-blur-sm 
              transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
            >
              <CardHeader>
                <!-- Step Badge -->
                <Badge variant="outline" class="mb-6 w-fit bg-primary/5">
                  <CheckCircle2 class="mr-1.5 h-3.5 w-3.5" />
                  {step.badge}
                </Badge>

                <CardContent class="p-0 flex items-start space-x-4">
                  <!-- Icon -->
                  <div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center shrink-0 
                    transition-colors group-hover:bg-primary/20">
                    <svelte:component
                      this={step.icon}
                      class="w-6 h-6 text-primary"
                      size={24}
                    />
                  </div>

                  <div>
                    <h3 class="font-semibold text-xl mb-2">{step.title}</h3>
                    <p class="text-muted-foreground">{step.description}</p>
                    
                    <!-- Hover State Arrow -->
                    <div class="mt-4 flex items-center text-sm font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
                      Learn more
                      <ArrowRight class="ml-1 h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </div>
                  </div>
                </CardContent>
              </CardHeader>
            </Card>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>