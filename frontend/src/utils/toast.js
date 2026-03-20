// Toast notification utility
export default {
  success(message, title = 'Success', duration = 5000) {
    this.show({ message, title, type: 'success', duration })
  },
  
  error(message, title = 'Error', duration = 7000) {
    this.show({ message, title, type: 'error', duration })
  },
  
  warning(message, title = 'Warning', duration = 6000) {
    this.show({ message, title, type: 'warning', duration })
  },
  
  info(message, title = 'Info', duration = 5000) {
    this.show({ message, title, type: 'info', duration })
  },
  
  show({ message, type = 'info', title = '', duration = 5000 }) {
    const event = new CustomEvent('show-toast', {
      detail: { message, type, title, duration }
    })
    window.dispatchEvent(event)
  }
}
