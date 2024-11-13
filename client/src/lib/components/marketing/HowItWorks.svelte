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

      <div class="relative">
        <!-- Timeline line - adjusted for better mobile view -->
        <div 
          class="absolute left-4 sm:left-4 inset-y-0 w-0.5 bg-gradient-to-b from-primary/50 via-primary/30 to-primary/50 
          md:left-1/2 md:-ml-0.5 rounded-full"
        ></div>
  
        <div class="space-y-8 relative">
          {#each steps as step, index}
            <div 
              class="flex flex-col md:flex-row items-start 
              {index % 2 === 0 ? 'md:flex-row-reverse' : ''} 
              relative pl-12 sm:pl-8 md:pl-0"
            >
              <div class="hidden md:block flex-1 md:w-1/2 md:px-8"></div>
              
              <!-- Timeline node - adjusted size and position -->
              <div 
                class="absolute left-0 md:static flex items-center justify-center w-8 h-8 md:w-10 md:h-10 
                rounded-full bg-primary text-primary-foreground shrink-0 md:mx-6 z-10 
                shadow-lg shadow-primary/20 transition-all duration-300 
                group-hover:scale-110 group-hover:shadow-xl"
              >
                <span class="font-bold text-sm md:text-base">{index + 1}</span>
              </div>
  
              <!-- Card - simplified for mobile -->
              <Card 
                class="flex-1 w-full md:w-1/2 md:px-8 group relative overflow-hidden 
                border border-primary/10 shadow-sm
                transition-all duration-300 hover:shadow-lg hover:shadow-primary/10
                hover:border-primary/20 mt-2 md:mt-0"
              >
                <CardHeader class="p-4 md:p-6">
                  <Badge 
                    variant="outline" 
                    class="mb-4 w-fit bg-primary/10 text-primary text-xs md:text-sm font-medium"
                  >
                    <CheckCircle2 class="mr-1.5 h-3 w-3 md:h-3.5 md:w-3.5" />
                    {step.badge}
                  </Badge>
  
                  <CardContent class="p-0 flex items-start space-x-3 md:space-x-4">
                    <div 
                      class="w-10 h-10 md:w-14 md:h-14 rounded-xl bg-primary/10 flex items-center justify-center shrink-0"
                    >
                      <svelte:component
                        this={step.icon}
                        class="w-5 h-5 md:w-7 md:h-7 text-primary"
                        size={24}
                      />
                    </div>
  
                    <div class="space-y-2">
                      <h3 class="font-semibold text-lg md:text-xl">{step.title}</h3>
                      <p class="text-muted-foreground text-sm md:text-base leading-relaxed">{step.description}</p>
                    </div>
                  </CardContent>
                </CardHeader>
              </Card>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</section>