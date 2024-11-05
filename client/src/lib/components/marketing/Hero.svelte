<script lang="ts">
  import { 
    GavelIcon, 
    ScaleIcon, 
    UploadIcon, 
    FileTextIcon, 
    MessageSquareIcon, 
    SearchIcon,
    ShieldCheckIcon,
    BookOpenIcon,
    CheckCircle2Icon,
    ArrowRightIcon,
    BarChart2Icon,
    ClockIcon
  } from 'lucide-svelte';
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { fade } from 'svelte/transition';
  import { tweened } from 'svelte/motion';
  
  interface Feature {
    icon: typeof GavelIcon;
    text: string;
    description: string;
  }

  interface StatItem {
    value: string;
    label: string;
  }

  type TabId = 'contracts' | 'litigation' | 'compliance';

  interface Tab {
    id: TabId;
    label: string;
  }

  let isCardHovered = false;
  let activeTab: TabId = 'contracts';
  let isTransitioning = false;

  const handleTabChange = (newTab: TabId) => {
    if (newTab === activeTab) return;
    
    isTransitioning = true;
    setTimeout(() => {
      activeTab = newTab;
      isTransitioning = false;
    }, 150);
  };
  
  const features: Record<TabId, Feature[]> = {
    contracts: [
      { 
        icon: FileTextIcon, 
        text: "Contract Analysis",
        description: "AI-powered contract review"
      },
      { 
        icon: BarChart2Icon, 
        text: "Risk Assessment",
        description: "Identify potential liabilities"
      },
      { 
        icon: SearchIcon, 
        text: "Clause Library",
        description: "Standard clause detection"
      },
      { 
        icon: ClockIcon, 
        text: "Version Control",
        description: "Track document changes"
      }
    ],
    litigation: [
      {
        icon: SearchIcon,
        text: "Case Research",
        description: "Precedent matching"
      },
      {
        icon: BarChart2Icon,
        text: "Outcome Prediction",
        description: "ML-based case analysis"
      },
      {
        icon: FileTextIcon,
        text: "Document Review",
        description: "Discovery automation"
      },
      {
        icon: ClockIcon,
        text: "Timeline Analysis",
        description: "Event sequencing"
      }
    ],
    compliance: [
      {
        icon: ShieldCheckIcon,
        text: "Regulation Tracking",
        description: "Stay up to date"
      },
      {
        icon: SearchIcon,
        text: "Policy Review",
        description: "Compliance verification"
      },
      {
        icon: BarChart2Icon,
        text: "Risk Monitoring",
        description: "Real-time alerts"
      },
      {
        icon: FileTextIcon,
        text: "Audit Reports",
        description: "Automated documentation"
      }
    ]
  };

  const stats: StatItem[] = [
    { value: "500+", label: "Am Law 200 Firms" },
    { value: "10B+", label: "Documents Processed" },
    { value: "99.98%", label: "Accuracy Rate" },
    { value: "85%", label: "Time Saved" }
  ];

  const trustIndicators: string[] = [
    "SOC 2 Type II Certified",
    "GDPR Compliant",
    "ISO 27001 Certified",
    "Bank-Grade Encryption"
  ];

  const tabs: Tab[] = [
    { id: 'contracts', label: 'Contract Review' },
    { id: 'litigation', label: 'Litigation Analysis' },
    { id: 'compliance', label: 'Compliance Check' }
  ];

  const riskLevels: Record<TabId, string> = {
    contracts: 'Low Risk',
    litigation: 'Medium Risk',
    compliance: 'Attention Needed'
  };

  const riskColors: Record<string, string> = {
    'Low Risk': 'text-green-500 bg-green-500/10',
    'Medium Risk': 'text-yellow-500 bg-yellow-500/10',
    'Attention Needed': 'text-red-500 bg-red-500/10'
  };
</script>

<div class="relative w-screen overflow-hidden bg-background text-foreground">
  <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(var(--primary-rgb),0.04),transparent_50%)]"></div>
  
  <div class="container relative mx-auto px-4 py-24 sm:px-6 lg:px-8">
    <div class="grid gap-16 lg:grid-cols-2">
      <!-- Left Column - Content -->
      <div class="relative z-10 flex flex-col justify-center space-y-12">
        <!-- Trust Badges -->
        <div class="flex flex-wrap gap-3">
          {#each trustIndicators as indicator}
            <Badge variant="outline" class="bg-background/80 backdrop-blur-sm">
              <CheckCircle2Icon class="mr-1.5 h-3.5 w-3.5" />
              {indicator}
            </Badge>
          {/each}
        </div>

        <!-- Main Content -->
        <div class="space-y-6">
          <h1 class="font-serif text-5xl font-bold tracking-tight sm:text-6xl xl:text-7xl">
            <span class="block text-muted-foreground">Elevate Your</span>
            <span class="relative mt-2 block text-primary">
              Legal Practice
              <svg class="absolute -bottom-2 left-0 h-2 w-full fill-none stroke-primary stroke-[4]" viewBox="0 0 100 10">
                <path d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5" vector-effect="non-scaling-stroke"/>
              </svg>
            </span>
          </h1>
          
          <p class="max-w-xl text-xl leading-relaxed text-muted-foreground">
            Transform legal workflows with AI-powered analysis, delivering unparalleled accuracy and efficiency for modern law practices.
          </p>
        </div>

        <!-- CTA Section -->
        <div class="flex flex-col gap-6 sm:flex-row">
          <Button size="lg" class="group relative px-8 py-6">
            <span class="relative z-10 flex items-center text-lg font-medium">
              Start Free Trial
              <ArrowRightIcon class="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
            </span>
          </Button>
          <Button size="lg" variant="outline" class="gap-2 px-8 py-6">
            <BookOpenIcon class="h-5 w-5" />
            <span class="text-lg font-medium">Schedule Demo</span>
          </Button>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 gap-8 border-t border-border pt-8 lg:grid-cols-4">
          {#each stats as { value, label }}
            <div class="relative">
              <div class="text-3xl font-bold text-primary">{value}</div>
              <div class="mt-1 text-sm text-muted-foreground">{label}</div>
            </div>
          {/each}
        </div>
      </div>

      <!-- Right Column - Interactive Demo -->
      <div class="relative">
        <!-- Tab Navigation -->
        <div class="mb-6 flex gap-4">
          {#each tabs as tab}
            <button
              class="relative px-4 py-2 text-sm font-medium transition-colors {activeTab === tab.id ? 'text-primary' : 'text-muted-foreground'}"
              on:click={() => handleTabChange(tab.id)}
            >
              {tab.label}
              {#if activeTab === tab.id}
                <div class="absolute -bottom-px left-0 h-0.5 w-full bg-primary"></div>
              {/if}
            </button>
          {/each}
        </div>

        <!-- Main Card -->
        <div class="relative">
          <!-- Background Cards -->
          <Card class="absolute -right-4 -top-4 h-full w-full bg-primary/5"></Card>
          <Card class="absolute -right-8 -top-8 h-full w-full bg-primary/5"></Card>

          <!-- Main Content Card -->
          <Card 
            class="relative z-10 overflow-hidden backdrop-blur-sm transition-all duration-500"
            on:mouseenter={() => isCardHovered = true}
            on:mouseleave={() => isCardHovered = false}
          >
            <!-- Card Header -->
            <div class="border-b border-border p-6">
              <div class="flex items-center justify-between">
                <Badge variant="outline" class="bg-primary/5 px-4 py-1.5">
                  <span class="relative flex h-2 w-2">
                    <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75"></span>
                    <span class="relative inline-flex h-2 w-2 rounded-full bg-primary"></span>
                  </span>
                  <span class="ml-2 font-medium">Live Analysis</span>
                </Badge>
                <div class="flex items-center gap-4">
                  <Badge variant="outline" class="gap-1.5">
                    <ClockIcon class="h-3.5 w-3.5" />
                    Real-time
                  </Badge>
                  <GavelIcon class="h-5 w-5 text-primary" />
                </div>
              </div>
            </div>

            <!-- Card Content -->
            <div class="space-y-8 p-6 transition-opacity duration-300" class:opacity-0={isTransitioning}>
              <!-- Analysis Progress -->
              <div class="space-y-4">
                <div class="flex justify-between">
                  <span class="text-sm font-medium">{tabs.find(t => t.id === activeTab)?.label}</span>
                  <span class="text-sm text-muted-foreground">84%</span>
                </div>
                <div class="h-2 rounded-full bg-primary/20">
                  <div class="h-full w-[84%] rounded-full bg-primary transition-all duration-500"></div>
                </div>
              </div>

              <!-- Feature Grid -->
              <div class="grid grid-cols-2 gap-6">
                {#each features[activeTab] as feature}
                  <div class="group space-y-2">
                    <div class="flex items-center gap-3">
                      <div class="rounded-lg bg-primary/10 p-2 transition-colors group-hover:bg-primary/20">
                        <svelte:component this={feature.icon} class="h-5 w-5 text-primary" />
                      </div>
                      <span class="font-medium">{feature.text}</span>
                    </div>
                    <p class="text-sm text-muted-foreground">{feature.description}</p>
                  </div>
                {/each}
              </div>

              <!-- Risk Indicators -->
              <div class="rounded-lg border border-border p-4">
                <div class="mb-4 flex items-center justify-between">
                  <span class="font-medium">Risk Assessment</span>
                  <Badge variant="outline" class={riskColors[riskLevels[activeTab]]}>
                    {riskLevels[activeTab]}
                  </Badge>
                </div>
                <div class="flex gap-4">
                  {#each Array(3) as _, i}
                    <div class="h-2 flex-1 rounded-full bg-primary/10">
                      <div 
                        class="h-full rounded-full bg-primary transition-all duration-500" 
                        style="width: {100 - (i * 30)}%"
                      ></div>
                    </div>
                  {/each}
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="mt-24 border-t border-border pt-12">
      <div class="flex flex-col items-center gap-8 text-center lg:flex-row lg:justify-between lg:text-left">
        <blockquote class="max-w-2xl text-xl font-medium italic text-muted-foreground">
          "This platform has fundamentally transformed our approach to legal analysis, saving hundreds of hours while improving accuracy."
        </blockquote>
        <div>
          <p class="font-serif text-lg">Katherine Chen, J.D.</p>
          <p class="text-sm text-muted-foreground">Managing Partner, Global Law LLP</p>
        </div>
      </div>
    </div>
  </div>
</div>