/**
 * Company Types Configuration
 * Maps company names/categories to their business type and required form fields
 */

export const COMPANY_TYPES = {
  BANKING: 'banking',
  INSURANCE: 'insurance',
  MEDICAL: 'medical',
  RETAIL: 'retail',
  CONSTRUCTION: 'construction',
  TECHNOLOGY: 'technology',
  REAL_ESTATE: 'real_estate',
  TELECOMMUNICATIONS: 'telecom',
  OTHER: 'other'
}

export const COMPANY_DATABASE = [
  {
    id: 1,
    name: 'ABSA Bank',
    type: COMPANY_TYPES.BANKING,
    logo: '🏦',
    requiredFields: ['card_type', 'account_number', 'employment_status'],
    products: [
      { id: 1, name: 'Credit Card', icon: '💳' },
      { id: 2, name: 'Debit Card', icon: '💳' },
      { id: 3, name: 'Savings Account', icon: '💰' },
      { id: 4, name: 'Investment Account', icon: '📈' },
      { id: 5, name: 'Home Loan', icon: '🏠' }
    ]
  },
  {
    id: 2,
    name: 'FNB (FirstRand Bank)',
    type: COMPANY_TYPES.BANKING,
    logo: '🏦',
    requiredFields: ['card_type', 'account_number', 'employment_status'],
    products: [
      { id: 1, name: 'Credit Card', icon: '💳' },
      { id: 2, name: 'Debit Card', icon: '💳' },
      { id: 3, name: 'Investment Account', icon: '📈' },
      { id: 4, name: 'Personal Loan', icon: '💵' }
    ]
  },
  {
    id: 3,
    name: 'Standard Bank',
    type: COMPANY_TYPES.BANKING,
    logo: '🏦',
    requiredFields: ['card_type', 'account_number', 'employment_status'],
    products: [
      { id: 1, name: 'Credit Card', icon: '💳' },
      { id: 2, name: 'Debit Card', icon: '💳' },
      { id: 3, name: 'Business Account', icon: '🏢' }
    ]
  },
  {
    id: 4,
    name: 'Discovery Health',
    type: COMPANY_TYPES.MEDICAL,
    logo: '🏥',
    requiredFields: ['medical_aid_type', 'coverage_level', 'dependents'],
    products: [
      { id: 1, name: 'Core Medical', icon: '🩺' },
      { id: 2, name: 'Comprehensive', icon: '🩺' },
      { id: 3, name: 'Budget', icon: '🏥' }
    ]
  },
  {
    id: 5,
    name: 'Momentum Health',
    type: COMPANY_TYPES.MEDICAL,
    logo: '🏥',
    requiredFields: ['medical_aid_type', 'coverage_level', 'dependents'],
    products: [
      { id: 1, name: 'Essential', icon: '🩺' },
      { id: 2, name: 'Optimal', icon: '🩺' },
      { id: 3, name: 'Premium', icon: '🏥' }
    ]
  },
  {
    id: 6,
    name: 'Liberty Group',
    type: COMPANY_TYPES.INSURANCE,
    logo: '📋',
    requiredFields: ['insurance_type', 'coverage_amount', 'risk_profile'],
    products: [
      { id: 1, name: 'Life Insurance', icon: '💼' },
      { id: 2, name: 'Short-term Insurance', icon: '🚗' },
      { id: 3, name: 'Income Protection', icon: '💪' }
    ]
  },
  {
    id: 7,
    name: 'Old Mutual',
    type: COMPANY_TYPES.INSURANCE,
    logo: '📋',
    requiredFields: ['insurance_type', 'coverage_amount', 'risk_profile'],
    products: [
      { id: 1, name: 'Life Insurance', icon: '💼' },
      { id: 2, name: 'Wealth Management', icon: '💎' },
      { id: 3, name: 'Retirement Planning', icon: '⏰' }
    ]
  },
  {
    id: 8,
    name: 'Telkom',
    type: COMPANY_TYPES.TELECOMMUNICATIONS,
    logo: '📱',
    requiredFields: ['service_type', 'data_bundle', 'contract_term'],
    products: [
      { id: 1, name: 'Mobile Plans', icon: '📱' },
      { id: 2, name: 'Fibre Broadband', icon: '📡' },
      { id: 3, name: 'Business Solutions', icon: '🏢' }
    ]
  },
  {
    id: 9,
    name: 'Vodacom',
    type: COMPANY_TYPES.TELECOMMUNICATIONS,
    logo: '📱',
    requiredFields: ['service_type', 'data_bundle', 'contract_term'],
    products: [
      { id: 1, name: 'Mobile Plans', icon: '📱' },
      { id: 2, name: 'Data Packages', icon: '📡' },
      { id: 3, name: 'Business Services', icon: '🏢' }
    ]
  }
]

/**
 * Get company by name (case-insensitive)
 */
export function findCompanyByName(name) {
  if (!name) return null
  const normalized = name.toLowerCase().trim()
  return COMPANY_DATABASE.find(c => c.name.toLowerCase().includes(normalized) || normalized.includes(c.name.toLowerCase()))
}

/**
 * Get all companies of a specific type
 */
export function getCompaniesByType(type) {
  return COMPANY_DATABASE.filter(c => c.type === type)
}

/**
 * Get required fields for a company
 */
export function getRequiredFields(companyId) {
  const company = COMPANY_DATABASE.find(c => c.id === companyId)
  return company ? company.requiredFields : []
}

/**
 * Get products for a company
 */
export function getCompanyProducts(companyId) {
  const company = COMPANY_DATABASE.find(c => c.id === companyId)
  return company ? company.products : []
}

/**
 * Get companies for autocomplete
 */
export function searchCompanies(query) {
  if (!query) return COMPANY_DATABASE.slice(0, 5)
  const normalized = query.toLowerCase()
  return COMPANY_DATABASE.filter(c =>
    c.name.toLowerCase().includes(normalized) ||
    c.type.includes(normalized)
  ).slice(0, 10)
}

/**
 * Field definitions for dynamic rendering
 */
export const DYNAMIC_FIELDS = {
  card_type: {
    label: 'Card Type',
    type: 'select',
    required: true,
    options: [
      { value: 'credit', label: 'Credit Card' },
      { value: 'debit', label: 'Debit Card' },
      { value: 'both', label: 'Both' }
    ]
  },
  account_number: {
    label: 'Account Number',
    type: 'text',
    required: true,
    placeholder: 'Enter your account number'
  },
  employment_status: {
    label: 'Employment Status',
    type: 'select',
    required: true,
    options: [
      { value: 'employed', label: 'Employed' },
      { value: 'self_employed', label: 'Self-Employed' },
      { value: 'retired', label: 'Retired' },
      { value: 'unemployed', label: 'Unemployed' }
    ]
  },
  medical_aid_type: {
    label: 'Medical Aid Type',
    type: 'select',
    required: true,
    options: [
      { value: 'core', label: 'Core' },
      { value: 'comprehensive', label: 'Comprehensive' },
      { value: 'essential', label: 'Essential' },
      { value: 'budget', label: 'Budget' }
    ]
  },
  coverage_level: {
    label: 'Coverage Level',
    type: 'select',
    required: true,
    options: [
      { value: 'individual', label: 'Individual' },
      { value: 'couple', label: 'Couple' },
      { value: 'family', label: 'Family' }
    ]
  },
  dependents: {
    label: 'Number of Dependents',
    type: 'number',
    required: false,
    placeholder: '0'
  },
  insurance_type: {
    label: 'Insurance Type',
    type: 'select',
    required: true,
    options: [
      { value: 'life', label: 'Life Insurance' },
      { value: 'short_term', label: 'Short-term Insurance' },
      { value: 'income_protection', label: 'Income Protection' }
    ]
  },
  coverage_amount: {
    label: 'Coverage Amount (ZAR)',
    type: 'number',
    required: true,
    placeholder: '500000'
  },
  risk_profile: {
    label: 'Risk Profile',
    type: 'select',
    required: true,
    options: [
      { value: 'low', label: 'Low Risk' },
      { value: 'moderate', label: 'Moderate Risk' },
      { value: 'high', label: 'High Risk' }
    ]
  },
  service_type: {
    label: 'Service Type',
    type: 'select',
    required: true,
    options: [
      { value: 'mobile', label: 'Mobile' },
      { value: 'fibre', label: 'Fibre Broadband' },
      { value: 'business', label: 'Business Solutions' }
    ]
  },
  data_bundle: {
    label: 'Data Bundle',
    type: 'select',
    required: true,
    options: [
      { value: '1gb', label: '1GB' },
      { value: '5gb', label: '5GB' },
      { value: '10gb', label: '10GB' },
      { value: 'unlimited', label: 'Unlimited' }
    ]
  },
  contract_term: {
    label: 'Contract Term (months)',
    type: 'select',
    required: true,
    options: [
      { value: 12, label: '12 months' },
      { value: 24, label: '24 months' },
      { value: 36, label: '36 months' }
    ]
  }
}
