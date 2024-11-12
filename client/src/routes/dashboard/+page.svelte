<script>
    import { fade } from 'svelte/transition';
</script>

<div class="flex flex-col items-center justify-center min-h-screen text-center bg-gray-100" in:fade>
    <h1 class="text-5xl text-gray-800 mb-4">Coming Soon</h1>
    <p class="text-xl text-gray-600 mb-8">We're working hard to bring you something amazing!</p>
    <div class="w-48 h-1 bg-gray-200 rounded overflow-hidden">
        <div class="w-1/3 h-full bg-green-500 animate-loading"></div>
    </div>
</div>

<style>
    @keyframes loading {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(400%); }
    }

    .animate-loading {
        animation: loading 2s infinite ease-in-out;
    }
</style>
