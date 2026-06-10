from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Competitor:
    """Core competitor record."""
    company_name: str
    website: str
    source: str
    source_url: str
    description: str = ""
    country: str = ""
    language: str = "en"
    category: str = ""
    competitor_type: str = "direct"
    confidence_score: float = 1.0
    notes: str = ""
    discovered_at: str = ""

    def __post_init__(self):
        if not self.discovered_at:
            self.discovered_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LandingPageAnalysis:
    """Website and landing page structure."""
    company_name: str
    website: str
    homepage_sections: List[str]
    hero_type: str
    cta_style: str
    social_proof_elements: List[str]
    offers: List[str]
    use_cases: List[str]
    industry_focus: List[str]
    lead_magnets: List[str]
    design_patterns: List[str]
    missing_sections: List[str]
    analysis_date: str = ""

    def __post_init__(self):
        if not self.analysis_date:
            self.analysis_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SEOAnalysis:
    """SEO and GEO gap analysis."""
    company_name: str
    website: str
    target_keywords: List[str]
    competitor_ranking_urls: Dict[str, str]
    recommended_url_types: List[str]
    content_gaps: List[str]
    seo_priority_score: float
    geo_opportunities: List[str]
    schema_recommendations: List[str]
    analysis_date: str = ""

    def __post_init__(self):
        if not self.analysis_date:
            self.analysis_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BlogAnalysis:
    """Blog content strategy."""
    company_name: str
    website: str
    blog_categories: List[str]
    top_blog_topics: List[str]
    content_gaps: List[str]
    recommended_posts: List[Dict[str, str]]
    topic_clusters: Dict[str, List[str]]
    analysis_date: str = ""

    def __post_init__(self):
        if not self.analysis_date:
            self.analysis_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LinkedInTrend:
    """LinkedIn trends and content insights."""
    trend_title: str
    description: str
    sources: List[str]
    pain_points: List[str]
    use_cases: List[str]
    post_hooks: List[str]
    carousel_outline: str
    cta_options: List[str]
    trend_date: str = ""

    def __post_init__(self):
        if not self.trend_date:
            self.trend_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineReport:
    """Final orchestrated report."""
    report_title: str
    generated_at: str
    competitors_discovered: int
    competitors_analyzed: int
    key_insights: List[str]
    recommendations: List[str]
    competitor_data: List[Dict[str, Any]]
    seo_gaps: List[Dict[str, Any]]
    blog_strategy: Dict[str, Any]
    linkedin_trends: List[Dict[str, Any]]
    next_steps: List[str]
