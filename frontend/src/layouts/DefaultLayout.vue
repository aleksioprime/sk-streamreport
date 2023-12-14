<template>
  <div class="default-layout">
    <default-header />
    <div class="default-content container">
      <slot />
    </div>
    <default-footer />
    
  </div>
</template>
  
<script setup>
import DefaultHeader from "./DefaultHeader.vue";
import DefaultFooter from "./DefaultFooter.vue";
</script>
  
<style lang="scss" scoped>
.default-content {
  min-height: calc(100vh - 220px);
  margin: 15px auto;
}
</style>