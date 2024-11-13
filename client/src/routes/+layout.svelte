<script>
  import DockedNavbar from "$lib/components/layout/DockedNavbar.svelte";
  import Footer from "$lib/components/layout/Footer.svelte";
  import * as Tooltip from "$lib/components/ui/tooltip/index";
  import { ModeWatcher } from "mode-watcher";
  import "../app.css";
</script>
<svelte:head>
  <title>Lexalyze - Legal Document Analysis</title>
  <meta name="description" content="Analyze legal documents with AI-powered insights and tools" />
  <meta name="keywords" content="legal analysis, document analysis, AI legal tools" />
  <meta property="og:title" content="Lexalyze - Legal Document Analysis" />
  <meta property="og:description" content="Analyze legal documents with AI-powered insights and tools" />
  <meta property="og:type" content="website" />
</svelte:head>
<Tooltip.Provider>
  <div
    class="min-h-screen flex justify-between w-screen flex-col hide-scrollbar"
  >
    <DockedNavbar /><ModeWatcher defaultMode={"dark"} />
    <slot />
    <Footer />
  </div></Tooltip.Provider
>
