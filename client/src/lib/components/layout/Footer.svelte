<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Card, CardContent } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { 
    Gavel, 
    Facebook, 
    Twitter, 
    Linkedin, 
    ArrowRight,
    Mail
  } from "lucide-svelte";

  const productLinks = ["Features", "Pricing", "Case Studies", "API"];
  const supportLinks = ["Documentation", "Guides", "FAQs", "Contact Us"];
  const companyLinks = ["About", "Blog", "Careers", "Press"];
  const legalLinks = ["Privacy Policy", "Terms of Service", "Cookie Policy", "GDPR Compliance"];

  const currentYear = new Date().getFullYear();
</script>

<footer class="relative bg-gradient-to-b from-background to-background/95 border-t py-24">
  <!-- Animated gradient background -->
  <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(var(--primary-rgb),0.07),transparent_70%)] animate-pulse"></div>
  
  <div class="container relative mx-auto px-6 lg:px-8">
    <div class="grid grid-cols-1 xl:grid-cols-12 gap-12">
      <!-- Brand Section -->
      <div class="xl:col-span-4 space-y-8">
        <div class="flex items-center space-x-3 group cursor-pointer">
          <img src="/logo-long-dark.png" alt="lexalyze logo" class="w-[80%]"/>
        </div>
        
        <p class="text-lg text-muted-foreground/90 max-w-md leading-relaxed">
          Revolutionizing legal document analysis with advanced AI technology, making legal work more efficient and accessible.
        </p>
        
        <Card class="bg-primary/5 border-primary/20 hover:border-primary/30 transition-colors">
          <CardContent class="p-4">
            <div class="flex space-x-8">
              <a href="#" class="text-muted-foreground hover:text-primary transition-all duration-200 hover:scale-110">
                <span class="sr-only">Facebook</span>
                <Facebook class="h-6 w-6" />
              </a>
              <a href="#" class="text-muted-foreground hover:text-primary transition-all duration-200 hover:scale-110">
                <span class="sr-only">Twitter</span>
                <Twitter class="h-6 w-6" />
              </a>
              <a href="#" class="text-muted-foreground hover:text-primary transition-all duration-200 hover:scale-110">
                <span class="sr-only">LinkedIn</span>
                <Linkedin class="h-6 w-6" />
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <!-- Links Sections -->
      <div class="xl:col-span-8 grid grid-cols-2 md:grid-cols-4 gap-8">
        <!-- Product Links -->
        <div>
          <Badge variant="outline" class="mb-6 px-3 py-1 text-sm font-medium">Product</Badge>
          <ul class="space-y-4">
            {#each productLinks as item}
              <li>
                <a href="#" class="group flex items-center text-base text-muted-foreground hover:text-primary transition-colors duration-200">
                  <ArrowRight class="mr-2 h-4 w-4 opacity-0 -translate-x-4 transition-all duration-200 group-hover:opacity-100 group-hover:translate-x-0" />
                  <span class="group-hover:translate-x-1 transition-transform duration-200">{item}</span>
                </a>
              </li>
            {/each}
          </ul>
        </div>

        <!-- Support Links -->
        <div>
          <Badge variant="outline" class="mb-6 px-3 py-1 text-sm font-medium">Support</Badge>
          <ul class="space-y-4">
            {#each supportLinks as item}
              <li>
                <a href="#" class="group flex items-center text-base text-muted-foreground hover:text-primary transition-colors duration-200">
                  <ArrowRight class="mr-2 h-4 w-4 opacity-0 -translate-x-4 transition-all duration-200 group-hover:opacity-100 group-hover:translate-x-0" />
                  <span class="group-hover:translate-x-1 transition-transform duration-200">{item}</span>
                </a>
              </li>
            {/each}
          </ul>
        </div>

        <!-- Company Links -->
        <div>
          <Badge variant="outline" class="mb-6 px-3 py-1 text-sm font-medium">Company</Badge>
          <ul class="space-y-4">
            {#each companyLinks as item}
              <li>
                <a href="#" class="group flex items-center text-base text-muted-foreground hover:text-primary transition-colors duration-200">
                  <ArrowRight class="mr-2 h-4 w-4 opacity-0 -translate-x-4 transition-all duration-200 group-hover:opacity-100 group-hover:translate-x-0" />
                  <span class="group-hover:translate-x-1 transition-transform duration-200">{item}</span>
                </a>
              </li>
            {/each}
          </ul>
        </div>

        <!-- Legal Links -->
        <div>
          <Badge variant="outline" class="mb-6 px-3 py-1 text-sm font-medium">Legal</Badge>
          <ul class="space-y-4">
            {#each legalLinks as item}
              <li>
                <a href="#" class="group flex items-center text-base text-muted-foreground hover:text-primary transition-colors duration-200">
                  <ArrowRight class="mr-2 h-4 w-4 opacity-0 -translate-x-4 transition-all duration-200 group-hover:opacity-100 group-hover:translate-x-0" />
                  <span class="group-hover:translate-x-1 transition-transform duration-200">{item}</span>
                </a>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    </div>
    
    <!-- Newsletter Section -->
    <div class="mt-16 border-t border-primary/10 pt-12">
      <Card class="bg-primary/5 border-primary/20 hover:border-primary/30 transition-colors overflow-hidden">
        <CardContent class="p-8">
          <div class="md:flex md:items-center md:justify-between gap-8">
            <div class="max-w-md">
              <Badge variant="outline" class="mb-4 px-3 py-1">
                <Mail class="mr-1.5 h-3.5 w-3.5" />
                Newsletter
              </Badge>
              <h3 class="text-2xl font-semibold mb-3">Stay Updated</h3>
              <p class="text-muted-foreground/90 leading-relaxed">
                Get the latest news, articles, and resources, sent directly to your inbox every week.
              </p>
            </div>
            <form class="mt-6 md:mt-0 flex flex-col sm:flex-row gap-3">
              <Input
                type="email"
                name="email"
                id="email"
                autocomplete="email"
                required
                placeholder="Enter your email"
                class="w-full sm:w-80 backdrop-blur-sm bg-background/50"
              />
              <Button type="submit" class="group whitespace-nowrap">
                Subscribe
                <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </form>
          </div>
        </CardContent>
      </Card>
      
      <p class="mt-8 text-sm text-muted-foreground/80 text-center">
        &copy; {currentYear} Lexalyze, Inc. All rights reserved.
      </p>
    </div>
  </div>
</footer>