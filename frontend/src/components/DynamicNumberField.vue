<template>
  <div>
    <label class="form-label">{{ fieldDef.label }} <span v-if="fieldDef.required" class="required">*</span></label>
    <input 
      class="form-input" 
      type="number"
      :value="value"
      :placeholder="fieldDef.placeholder || ''"
      :required="fieldDef.required"
      @input="$emit('input', $event.target.value)"
    >
  </div>
</template>

<script>
export default {
  name: 'DynamicNumberField',
  props: {
    fieldKey: String,
    fieldDef: Object,
    value: [String, Number]
  },
  emits: ['input']
}
</script>

<style scoped>
.required {
  color: #dc2626;
}
</style>
