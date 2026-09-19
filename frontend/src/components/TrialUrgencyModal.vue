<template>
  <!-- TrialUrgencyModal has been decommissioned. Corporate Sovereign is permanent R0 core. -->
  <div v-if="false"></div>
</template>

<script>
export default {
  name: 'TrialUrgencyModal',
  props: {
    show: Boolean,
    daysRemaining: Number,
    isInGrace: Boolean,
    graceDaysRemaining: Number,
    plan: String,
    planName: String,
    planPrice: [String, Number]
  },
  emits: ['close', 'acknowledge'],
  watch: {
    show(val) {
      if (val) {
        this.$emit('close')
        this.$emit('acknowledge')
      }
    }
  },
  mounted() {
    if (this.show) {
      this.$emit('close')
      this.$emit('acknowledge')
    }
  }
}
</script>
