<script>
  import DockedNavbar from "$lib/components/layout/DockedNavbar.svelte";
  import Footer from "$lib/components/layout/Footer.svelte";
  import * as Tooltip from "$lib/components/ui/tooltip/index";
  import "../app.css";
</script>

<Tooltip.Provider
  ><div class="min-h-screen flex justify-between w-screen dark flex-col hide-scrollbar">
    <DockedNavbar />
    <slot />
    <Footer />
  </div></Tooltip.Provider
>
