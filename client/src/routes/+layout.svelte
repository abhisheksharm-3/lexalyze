<script>
  import DockedNavbar from "$lib/components/layout/DockedNavbar.svelte";
  import Footer from "$lib/components/layout/Footer.svelte";
  import * as Tooltip from "$lib/components/ui/tooltip/index";
  import { ModeWatcher } from "mode-watcher";
  import "../app.css";
</script>

<Tooltip.Provider>
  <div
    class="min-h-screen flex justify-between w-screen flex-col hide-scrollbar"
  >
    <DockedNavbar /><ModeWatcher defaultMode={"dark"} />
    <slot />
    <Footer />
  </div></Tooltip.Provider
>
