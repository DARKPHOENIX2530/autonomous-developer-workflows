// Legacy Frontend Types (Drifted from v2.4.0 backend)
export interface Subscription {
  id: string;
  customer_id: string; // BREAKING: Backend renamed this to camelCase `customerId`!
  tier: string;        // BREAKING: Backend renamed this to `planTier`!
  status: string;
  // MISSING: `renewalDate: string`
  // MISSING: `isMfaEnforced: boolean`
}
