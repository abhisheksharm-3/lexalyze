<script lang="ts">
    import {
      GavelIcon,
      ScaleIcon,
      FileTextIcon,
      MessageSquareIcon,
      SearchIcon,
      UsersIcon,
      BookOpenIcon,
      PhoneCallIcon,
      ClockIcon,
      DollarSignIcon,
    } from 'lucide-svelte';
    import * as Tooltip from "$lib/components/ui/tooltip/index";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import Dock from "$lib/components/ui/dock/Dock.svelte";
    import DockIcons from "$lib/components/ui/dock/DockIcons.svelte";
  
    let navs = {
      mainServices: [
        { label: "Legal Consultation", icon: GavelIcon, href: "/consultation" },
        { label: "Document Review", icon: FileTextIcon, href: "/documents" },
        { label: "Case Analysis", icon: ScaleIcon, href: "/analysis" },
        { label: "Legal Research", icon: SearchIcon, href: "/research" },
      ],
      additionalServices: [
        { label: "Knowledge Base", icon: BookOpenIcon, href: "/resources" },
        { label: "Contact Us", icon: PhoneCallIcon, href: "/contact" },
        { label: "Pricing", icon: DollarSignIcon, href: "/pricing" },
      ],
    };
  </script>
  
  <div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50">
    
    <div class="mt-8">
      <Dock direction="middle" class="bg-background/80 backdrop-blur-lg border border-border/50 shadow-lg" let:mouseX let:distance let:magnification>
        {#each navs.mainServices as item}
          <DockIcons {mouseX} {magnification} {distance}>
            <Tooltip.Root>
              <Tooltip.Trigger
                class="hover:bg-primary/20 transition-all duration-200 rounded-full p-3 mx-0"
              >
                <svelte:component 
                  this={item.icon} 
                  size={24} 
                  strokeWidth={1.5}
                  class="text-primary"
                />
              </Tooltip.Trigger>
              <Tooltip.Content side="bottom" sideOffset={8} class="bg-primary/90 text-primary-foreground">
                <p class="text-sm font-medium">{item.label}</p>
              </Tooltip.Content>
            </Tooltip.Root>
          </DockIcons>
        {/each}
  
        <Separator orientation="vertical" class="h-full w-[0.6px] mx-2 bg-primary/20" />
  
        {#each navs.additionalServices as item}
          <DockIcons {mouseX} {magnification} {distance}>
            <Tooltip.Root>
              <Tooltip.Trigger
                class="hover:bg-primary/20 transition-all duration-200 rounded-full p-3 mx-0"
              >
                <svelte:component 
                  this={item.icon} 
                  size={24} 
                  strokeWidth={1.5}
                  class="text-primary"
                />
              </Tooltip.Trigger>
              <Tooltip.Content side="bottom" sideOffset={8} class="bg-primary/90 text-primary-foreground">
                <p class="text-sm font-medium">{item.label}</p>
              </Tooltip.Content>
            </Tooltip.Root>
          </DockIcons>
        {/each}
      </Dock>
    </div>
  </div>