<template>

  <div class="flex h-screen gap-1">
    <PanelMenu class="w-full" v-model="selected" :model="ite"/>
    <Divider layout="vertical" style="height: max()"/>

  </div>


</template>


<script setup>

const selected = ref();

const props = defineProps(['data', 'dataKey', 'command'])

const ite = props.data?.map(obj => ({
  label: `Week-${obj.number}`,
  items: obj[props.dataKey]?.map(item => ({
    label: `${item.title}`,
    command: ()=> {
      props.command(item)
    }
  }))
}))


</script>


<style scoped>

</style>