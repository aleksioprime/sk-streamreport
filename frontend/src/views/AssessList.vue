<template>
    <div>
        <base-header>
            <template v-slot:header>Итоговые работы</template>
        </base-header>
        <button type="button" class="btn btn-primary ms-auto mb-2 w-100" @click="showSumAssess">
          Cоздать итоговую работу
        </button>
    </div>
    

</template>

<script>
export default {
    name: 'Assessment',
    data() {
        return {

        }
    },
    methods: {
        showSumAssess() {
            console.log('Success')
        }
    }
}
</script>

<style>

</style>