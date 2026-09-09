<template>
  <div class="admin-layout">
    <AdminSidebar />
    <main class="admin-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f7f3ee;
}

.admin-content {
  min-height: 100vh;
  margin-left: 17rem;
  padding: 2rem clamp(1.25rem, 4vw, 4rem);
}

@media (max-width: 767px) {
  .admin-content {
    margin-left: 0;
    padding: 5rem 1rem 2rem;
  }
}
</style>
