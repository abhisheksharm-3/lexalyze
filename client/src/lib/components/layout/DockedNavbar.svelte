<script lang="ts">
  import ModeToggle from './../ModeToggle.svelte';
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
    Home,
    LayoutDashboard,
    Info,
  } from 'lucide-svelte';
  import * as Tooltip from "$lib/components/ui/tooltip/index";
  import Separator from "$lib/components/ui/separator/separator.svelte";
  import Dock from "$lib/components/ui/dock/Dock.svelte";
  import DockIcons from "$lib/components/ui/dock/DockIcons.svelte";

  let navs = {
    mainServices: [
      { label: "Home", icon: Home, href: "/" },
      { label: "Analyze", icon: ScaleIcon, href: "/analyze" },
      { label: "Dashboard", icon: LayoutDashboard, href: "/dashboard" },
    ],
    additionalServices: [
      { label: "About Us", icon: Info, href: "/about" },
    ],
  };  
</script>

<div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50">
  <div class="mt-8">
    <Dock direction="middle" class="bg-background/80 backdrop-blur-lg border border-border/50 shadow-lg z-50" let:mouseX let:distance let:magnification>
      {#each navs.mainServices as item}
        <DockIcons {mouseX} {magnification} {distance}>
          <a href={item.href} class="block">
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
          </a>
        </DockIcons>
      {/each}

      <Separator orientation="vertical" class="h-full w-[0.6px] mx-2 bg-primary/20" />

      {#each navs.additionalServices as item}
        <DockIcons {mouseX} {magnification} {distance}>
          <a href={item.href} class="block">
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
          </a>
        </DockIcons>
      {/each}
      <Separator orientation="vertical" class="h-full w-[0.6px] mx-2 bg-primary/20" />
      <ModeToggle />
    </Dock>
  </div>
</div>