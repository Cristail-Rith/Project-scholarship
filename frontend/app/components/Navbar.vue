<template>
    <div>
        <nav class="sticky t-0 ma-0 w-full flex h-full bg-[#d9eae5] justify-between p-7 mt-8">
            <div>
                <ul class="flex gap-10">
                    <li><nuxt-link to="/" class="nav-link">HOME</nuxt-link></li>
                    <li><nuxt-link to="/menu" class="nav-link">MENU</nuxt-link></li>
                    <li><nuxt-link to="/table" class="nav-link" >DINING TABLE</nuxt-link></li>
                </ul>
            </div>
            <div class=" ">
                logo
            </div>

            <div>
                <ul class="flex gap-10">
                    <li><nuxt-link to="/orders" class="nav-link">ORDERS</nuxt-link></li>
                    <li><nuxt-link to="/about" class="nav-link">ABOUT</nuxt-link></li>
                </ul>
                <div>
                    
                </div>
            </div>  
        </nav>
    </div>
</template>

<script>
</script>

<style>
.nav-link {
    position: relative;
    padding-bottom: 4px;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #047857;
    transition: width 0.3s ease;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
    width: 100%;
}
</style>
