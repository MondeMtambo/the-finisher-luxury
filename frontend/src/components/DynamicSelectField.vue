<template>
  <div>
    <label class="form-label">{{ fieldDef.label }} <span v-if="fieldDef.required" class="required">*</span></label>
    <select class="form-input" :value="value" @input="$emit('input', $event.target.value)" :required="fieldDef.required">
      <option value="">{{ fieldDef.placeholder || 'Select...' }}</option>
      <option v-for="opt in fieldDef.options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'DynamicSelectField',
  props: {
    fieldKey: String,
    fieldDef: Object,
    value: String
  },
  emits: ['input']
}
</script>

<style scoped>
.required {
  color: #dc2626;
}
</style>
