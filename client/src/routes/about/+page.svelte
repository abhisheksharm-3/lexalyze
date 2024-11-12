<script lang="ts">
  import { 
    BrainCircuitIcon,
    CodeIcon,
    BookOpenIcon,
    RocketIcon,
    GithubIcon,
    LinkedinIcon,
    TwitterIcon,
    GraduationCapIcon,
    MessagesSquareIcon,
    SparklesIcon,
    DatabaseIcon
  } from 'lucide-svelte';
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  
  interface Project {
    title: string;
    description: string;
    tags: string[];
    icon: any;
  }

  interface Research {
    area: string;
    description: string;
    icon: any;
  }

  const projects: Project[] = [
    {
      title: "Sentiment Analysis Engine",
      description: "Advanced sentiment analysis using transformer models",
      tags: ["PyTorch", "BERT", "NLP"],
      icon: MessagesSquareIcon
    },
    {
      title: "Text Summarization",
      description: "Extractive and abstractive summarization pipeline",
      tags: ["Transformers", "Python", "ML"],
      icon: SparklesIcon
    },
    {
      title: "NLP Dataset Tools",
      description: "Tools for processing and analyzing text datasets",
      tags: ["Python", "pandas", "NLP"],
      icon: DatabaseIcon
    }
  ];

  const research: Research[] = [
    {
      area: "Natural Language Processing",
      description: "Focusing on transformer architectures and their applications in understanding human language",
      icon: BrainCircuitIcon
    },
    {
      area: "Machine Learning",
      description: "Exploring neural architectures for language understanding and generation",
      icon: CodeIcon
    },
    {
      area: "Text Analysis",
      description: "Developing tools for automated text processing and analysis",
      icon: BookOpenIcon
    }
  ];

  const stack = [
    "Python", "PyTorch", "TensorFlow",
    "Transformers", "spaCy", "NLTK",
    "FastAPI", "SvelteKit", "Svelte"
  ];

  // Update these with your actual links
  const socialLinks = {
    github: "https://github.com/abhisheksharm-3",
    linkedin: "https://linkedin.com/in/abhisheksan",
    twitter: "https://twitter.com/iabhisheksan"
  };
</script>

<div class="relative w-full bg-background text-foreground">
  <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(var(--primary-rgb),0.04),transparent_50%)]"></div>
  
  <div class="container relative mx-auto px-4 py-24 sm:px-6 lg:px-8">
    <!-- Hero Section -->
    <div class="mb-24">
      <div class="flex flex-col-reverse lg:grid lg:grid-cols-2 lg:gap-16 items-center">
        <div class="mt-12 lg:mt-0">
          <Badge variant="outline" class="mb-6">
            <BrainCircuitIcon class="mr-1.5 h-3.5 w-3.5" />
            NLP Research
          </Badge>
          
          <h1 class="font-serif text-4xl sm:text-5xl font-bold tracking-tight mb-6">
            <span class="block text-muted-foreground">Welcome to</span>
            <span class="relative mt-2 block text-primary">
              NLP Lab
              <svg class="absolute -bottom-2 left-0 h-2 w-full fill-none stroke-primary stroke-[4]" viewBox="0 0 100 10">
                <path d="M 0 5 Q 25 0, 50 5 Q 75 10, 100 5" vector-effect="non-scaling-stroke"/>
              </svg>
            </span>
          </h1>
          
          <p class="text-xl text-muted-foreground mb-8">
            A personal research laboratory exploring the frontiers of Natural Language Processing
            and Machine Learning.
          </p>

          <div class="flex gap-4">
            <Button size="lg" class="gap-2">
              <RocketIcon class="h-4 w-4" />
              View Projects
            </Button>
            <Button variant="outline" size="lg" class="gap-2">
              <GithubIcon class="h-4 w-4" />
              GitHub
            </Button>
          </div>
        </div>

        <Card class="relative">
          <div class="absolute -right-4 -top-4 h-full w-full bg-primary/5 rounded-lg"></div>
          <div class="absolute -right-8 -top-8 h-full w-full bg-primary/5 rounded-lg"></div>
          
          <Card class="relative p-6 space-y-6">
            <div class="flex items-center gap-4">
              <div class="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
                <img 
                  src="https://github.com/abhisheksharm-3.png" 
                  alt="Abhishek Sharma" 
                  class="h-14 w-14 rounded-full object-cover"
                />
              </div>
              <div>
                <h2 class="text-xl font-bold">Abhishek Sharma</h2>
                <p class="text-sm text-muted-foreground">ML Engineer & NLP Researcher</p>
              </div>
            </div>

            <div class="flex gap-3">
              {#each Object.entries(socialLinks) as [platform, url]}
                <a href={url} target="_blank" rel="noopener noreferrer">
                  <Button variant="ghost" size="icon" class="h-9 w-9">
                    <svelte:component this={{
                      github: GithubIcon,
                      linkedin: LinkedinIcon,
                      twitter: TwitterIcon
                    }[platform]} class="h-4 w-4" />
                  </Button>
                </a>
              {/each}
            </div>

            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <GraduationCapIcon class="h-4 w-4 text-primary" />
                <span class="text-sm">ML/NLP Specialist</span>
              </div>
              <div class="flex items-center gap-2">
                <CodeIcon class="h-4 w-4 text-primary" />
                <span class="text-sm">Full Stack Developer</span>
              </div>
            </div>
          </Card>
        </Card>
      </div>
    </div>

    <!-- Research Areas -->
    <div class="mb-24">
      <h2 class="text-center font-serif text-3xl font-bold mb-12">Research Focus</h2>
      <div class="grid gap-8 md:grid-cols-3">
        {#each research as { area, description, icon }}
          <Card class="p-6 transition-all hover:shadow-lg">
            <div class="mb-4 rounded-lg bg-primary/10 p-3 w-fit">
              <svelte:component this={icon} class="h-6 w-6 text-primary" />
            </div>
            <h3 class="mb-2 font-bold">{area}</h3>
            <p class="text-sm text-muted-foreground">{description}</p>
          </Card>
        {/each}
      </div>
    </div>

    <!-- Projects Section -->
    <div class="mb-24">
      <h2 class="text-center font-serif text-3xl font-bold mb-12">Featured Projects</h2>
      <div class="grid gap-8 md:grid-cols-3">
        {#each projects as { title, description, tags, icon }}
          <Card class="p-6">
            <div class="mb-4 rounded-lg bg-primary/10 p-3 w-fit">
              <svelte:component this={icon} class="h-6 w-6 text-primary" />
            </div>
            <h3 class="mb-2 font-bold">{title}</h3>
            <p class="text-sm text-muted-foreground mb-4">{description}</p>
            <div class="flex flex-wrap gap-2">
              {#each tags as tag}
                <Badge variant="secondary" class="text-xs">{tag}</Badge>
              {/each}
            </div>
          </Card>
        {/each}
      </div>
    </div>

    <!-- Tech Stack -->
    <div class="mb-24">
      <h2 class="text-center font-serif text-3xl font-bold mb-12">Tech Stack</h2>
      <Card class="p-8">
        <div class="flex flex-wrap justify-center gap-3">
          {#each stack as technology}
            <Badge variant="outline" class="px-4 py-2">
              {technology}
            </Badge>
          {/each}
        </div>
      </Card>
    </div>

    <!-- Contact Section -->
    <div class="text-center">
      <Card class="mx-auto max-w-3xl p-12">
        <h2 class="mb-4 font-serif text-3xl font-bold">Let's Connect</h2>
        <p class="mb-8 text-muted-foreground">
          Interested in collaborating on NLP research or have questions about my projects?
        </p>
        <div class="flex justify-center gap-4">
          <Button size="lg" class="gap-2">
            <MessagesSquareIcon class="h-4 w-4" />
            Get in Touch
          </Button>
          <Button variant="outline" size="lg" class="gap-2">
            <GithubIcon class="h-4 w-4" />
            View Code
          </Button>
        </div>
      </Card>
    </div>
  </div>
</div>