/**
 * Modern confirm/alert/prompt dialog utility.
 * Uses the ConfirmModal component via custom events.
 *
 * Usage:
 *   import modal from '../utils/modal'
 *
 *   // Alert (no cancel button)
 *   await modal.alert('Title', 'Message')
 *
 *   // Confirm (OK / Cancel)
 *   const ok = await modal.confirm('Delete?', 'This cannot be undone.', 'danger')
 *
 *   // Prompt (input field)
 *   const value = await modal.prompt('Enter password', 'Min 8 characters', { inputType: 'password' })
 */

function dispatch(detail) {
  return new Promise(resolve => {
    window.dispatchEvent(new CustomEvent('show-confirm', {
      detail: {
        ...detail,
        _resolve: resolve
      }
    }))
  })
}

export default {
  /**
   * Show alert dialog (single OK button)
   */
  alert(title, message, type = 'info') {
    return dispatch({ title, message, type, showCancel: false, confirmText: 'Got It' })
  },

  /**
   * Show success alert
   */
  success(title, message) {
    return dispatch({ title, message, type: 'success', showCancel: false, confirmText: 'Awesome!' })
  },

  /**
   * Show error alert
   */
  error(title, message) {
    return dispatch({ title, message, type: 'error', showCancel: false, confirmText: 'OK' })
  },

  /**
   * Show warning alert
   */
  warning(title, message) {
    return dispatch({ title, message, type: 'warning', showCancel: false, confirmText: 'Understood' })
  },

  /**
   * Show confirm dialog (OK / Cancel)
   */
  confirm(title, message, type = 'warning', { confirmText = 'Confirm', cancelText = 'Cancel' } = {}) {
    return dispatch({ title, message, type, showCancel: true, confirmText, cancelText })
  },

  /**
   * Show danger confirm dialog (delete actions)
   */
  danger(title, message, { confirmText = 'Delete', cancelText = 'Keep' } = {}) {
    return dispatch({ title, message, type: 'danger', showCancel: true, confirmText, cancelText })
  },

  /**
   * Show prompt dialog with input field
   */
  prompt(title, message, { type = 'info', inputType = 'text', inputPlaceholder = '', confirmText = 'Submit', cancelText = 'Cancel' } = {}) {
    return dispatch({ title, message, type, showCancel: true, showInput: true, inputType, inputPlaceholder, confirmText, cancelText })
  },

  /**
   * Show payment-themed dialog
   */
  payment(title, message, { confirmText = 'Proceed to Payment', cancelText = 'Later' } = {}) {
    return dispatch({ title, message, type: 'payment', showCancel: true, confirmText, cancelText })
  }
}
