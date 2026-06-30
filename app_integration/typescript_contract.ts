export type ReviewStatus = 'draft' | 'needs_source' | 'reviewed' | 'generated' | 'mined' | 'unknown';

export interface IngredientAlias {
  ingredient_id: string;
  canonical_name: string;
  alias: string;
  normalized_alias: string;
  source_file?: string;
  review_status: ReviewStatus;
}

export interface IngredientFact {
  fact_id: string;
  ingredient_id: string;
  canonical_name: string;
  fact_type: string;
  fact_text: string;
  evidence_level: string;
  review_status: ReviewStatus;
  citation_id?: string;
}

export interface RegulatoryStatus {
  regulatory_id: string;
  ingredient_id: string;
  canonical_name: string;
  jurisdiction: string;
  status: string;
  allowed_use_notes: string;
  requires_warning: 'yes' | 'no' | string;
  review_status: ReviewStatus;
  citation_id?: string;
  notes?: string;
}

export interface IngredientHistory {
  history_id: string;
  ingredient_id: string;
  canonical_name: string;
  history_estimate: string;
  confidence: string;
  region_or_origin: string;
  notes: string;
  review_status: ReviewStatus;
  citation_id?: string;
}

export interface DisplaySafety {
  can_show_as_verified: boolean;
  requires_uncertainty_label: boolean;
  hide_medical_claims: boolean;
}

export interface EvidencePack {
  ingredient_id: string;
  canonical_name: string;
  category: string;
  subcategory: string;
  source_type: string;
  functional_purpose: string;
  common_foods: string;
  app_note: string;
  risk_note: string;
  review_status: ReviewStatus;
  source_file: string;
  aliases: IngredientAlias[];
  facts: IngredientFact[];
  regulatory_status: RegulatoryStatus[];
  history: IngredientHistory[];
  display_safety: DisplaySafety;
}

export interface LabelMatch {
  raw_term: string;
  normalized_term: string;
  ingredient_id: string;
  canonical_name: string;
  match_type: 'exact_alias' | 'ocr_alias' | 'fuzzy' | 'manual';
  confidence: number;
  review_status: ReviewStatus;
}

export interface LabelAnalysisResult {
  original_text: string;
  jurisdiction: string;
  matched_ingredients: LabelMatch[];
  unmatched_terms: string[];
  warnings?: string[];
  uncertainty_notes: string[];
}

export interface ScanBadge {
  badge_id: string;
  badge_name: string;
  badge_type: string;
  trigger_logic: string;
  display_priority: string;
  color_hint: string;
  icon_hint: string;
  public_copy: string;
  review_status: ReviewStatus;
}

export interface ReportSection {
  section_id: string;
  section_name: string;
  section_order: string;
  default_state: 'expanded' | 'collapsed' | string;
  description: string;
  data_sources: string;
  app_copy_template: string;
  review_status: ReviewStatus;
}
