import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Philosophical AI Journalist",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .philosophy-card {
        background: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF4B4B;
        margin: 1rem 0;
    }
    .generation-status {
        background: #1E1E1E;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# Philosophical Frameworks
PHILOSOPHICAL_FRAMEWORKS = {
    "human_experience": {
        "name": "Human Experience",
        "thinkers": ["Aristotle", "Hannah Arendt", "Albert Camus"],
        "core_questions": [
            "What does this mean for human flourishing?",
            "How does this impact daily lived experience?",
            "What are the emotional and psychological dimensions?"
        ],
        "color": "#FF6B6B"
    },
    "ethical_dimension": {
        "name": "Ethical Dimension", 
        "thinkers": ["Immanuel Kant", "John Stuart Mill", "Martha Nussbaum"],
        "core_questions": [
            "What are the moral implications and consequences?",
            "Who benefits and who bears the costs?",
            "What principles of justice apply?"
        ],
        "color": "#4ECDC4"
    },
    "systems_thinking": {
        "name": "Systems Thinking",
        "thinkers": ["Karl Marx", "Michel Foucault", "Donna Haraway"],
        "core_questions": [
            "What larger systems and structures are at play?",
            "What power dynamics are involved?",
            "How are different elements interconnected?"
        ],
        "color": "#45B7D1"
    },
    "existential_reflection": {
        "name": "Existential Reflection",
        "thinkers": ["Jean-Paul Sartre", "Simone de Beauvoir", "Friedrich Nietzsche"],
        "core_questions": [
            "What does this reveal about human freedom and responsibility?",
            "How does this shape identity and meaning?",
            "What authentic responses are possible?"
        ],
        "color": "#96CEB4"
    }
}

# Free AI Models
FREE_MODELS = {
    "creative": {
        "name": "🤖 Kat Coder Pro (Creative)",
        "id": "kwaipilot/kat-coder-pro:free",
        "strengths": ["Narrative writing", "Creative expression", "Storytelling"]
    },
    "analytical": {
        "name": "🦙 Nemotron Nano (Analytical)", 
        "id": "nvidia/nemotron-nano-12b-vl:free",
        "strengths": ["Structured analysis", "Logical reasoning", "Technical clarity"]
    },
    "balanced": {
        "name": "💎 Gemma 2B (Balanced)",
        "id": "google/gemma-2-9b-it:free",
        "strengths": ["General purpose", "Balanced responses", "Reliable performance"]
    }
}

class PhilosophicalWriter:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def get_headers(self, api_key):
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://philosophical-ai-journalist.streamlit.app",
            "X-Title": "Philosophical AI Journalist"
        }
    
    def construct_quick_insight_prompt(self, topic, framework, tone):
        framework_info = PHILOSOPHICAL_FRAMEWORKS[framework]
        
        prompt = f"""As a philosophical journalist, analyze this topic: "{topic}"

PHILOSOPHICAL LENS: {framework_info['name']}
KEY THINKERS: {', '.join(framework_info['thinkers'])}
CORE QUESTIONS: {'; '.join(framework_info['core_questions'])}

Write a 400-600 word article with this 3-layer structure:

1. THE HUMAN STORY: Start with a compelling narrative or personal example that makes this topic relatable and concrete.

2. PHILOSOPHICAL ANALYSIS: Apply the {framework_info['name']} perspective using insights from {framework_info['thinkers'][0]} and {framework_info['thinkers'][1]}. Connect to the core questions about {framework_info['core_questions'][0].lower()}

3. ACTIONABLE INSIGHTS: Provide practical takeaways, questions for further reflection, or suggestions for how readers can engage with these ideas.

TONE: {tone.upper()} - Maintain this tone throughout.

Focus on making complex philosophical ideas accessible and relevant to contemporary readers."""
        
        return prompt
    
    def construct_deep_analysis_prompt(self, topic, framework, tone):
        framework_info = PHILOSOPHICAL_FRAMEWORKS[framework]
        
        prompt = f"""As a philosophical journalist, conduct a deep analysis of: "{topic}"

PHILOSOPHICAL FRAMEWORK: {framework_info['name']}
THINKERS: {', '.join(framework_info['thinkers'])}

Write a comprehensive 800-1200 word article with this 7-layer structure:

1. HUMAN NARRATIVE: Begin with a vivid, relatable story or example that grounds the topic in human experience.

2. HISTORICAL CONTEXT: Place the topic in broader historical and cultural context. How have similar issues evolved?

3. PHILOSOPHICAL DEPTH: Apply {framework_info['name']} perspective using {framework_info['thinkers'][0]}'s framework for {framework_info['core_questions'][0].split('?')[0].lower()}.

4. INTERCONNECTIONS: Explore how {framework_info['thinkers'][1]}'s ideas about {framework_info['core_questions'][1].split('?')[0].lower()} relate to this topic.

5. CRITICAL REFLECTION: Incorporate {framework_info['thinkers'][2]}'s perspective to challenge assumptions and reveal hidden dimensions.

6. CONTEMPORARY RELEVANCE: Connect these philosophical insights to current events, technologies, or social trends.

7. TRANSFORMATIVE INSIGHTS: Provide profound takeaways, reflective questions, and practical applications for readers.

TONE: {tone.upper()} - Maintain philosophical depth while ensuring accessibility.

Weave these layers together seamlessly, creating an article that enlightens and transforms the reader's understanding."""
        
        return prompt
    
    def generate_article(self, api_key, model_id, prompt, analysis_type):
        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a philosophical journalist who makes complex ideas accessible and meaningful. You write with clarity, depth, and practical relevance."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 1200 if analysis_type == "deep" else 800,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.get_headers(api_key),
                json=payload,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'], None
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                return None, error_msg
                
        except requests.exceptions.Timeout:
            return None, "Request timed out. Free models can be slow. Please try again."
        except Exception as e:
            return None, f"Error: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Philosophical AI Journalist</h1>', unsafe_allow_html=True)
    st.markdown("### Transform topics into deeply insightful articles with philosophical perspectives")
    
    # Initialize session state
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'generated_article' not in st.session_state:
        st.session_state.generated_article = None
    if 'generation_metrics' not in st.session_state:
        st.session_state.generation_metrics = None
    
    # Sidebar - Authentication
    with st.sidebar:
        st.header("🔑 Authentication")
        st.markdown("""
        **Get Your FREE API Key:**
        1. Visit [OpenRouter](https://openrouter.ai/keys)
        2. Sign up with Google/GitHub (30 seconds)
        3. Create & paste your API key below
        """)
        
        api_key = st.text_input("OpenRouter API Key:", type="password", 
                               placeholder="sk-or-...", value=st.session_state.api_key)
        
        if api_key:
            if api_key.startswith('sk-or-'):
                st.session_state.api_key = api_key
                st.success("✅ API Key Validated")
            else:
                st.error("❌ Invalid API Key format")
        
        st.markdown("---")
        st.header("🎯 Quick Start")
        
        # Quick start templates
        template = st.selectbox("Or try a template:", 
                               ["Custom Topic", "AI & Creativity", "Remote Work Impact", "Climate Change Ethics"])
        
        if template != "Custom Topic":
            if template == "AI & Creativity":
                default_topic = "How artificial intelligence is transforming human creativity and artistic expression"
                default_framework = "human_experience"
            elif template == "Remote Work Impact":
                default_topic = "How remote work is fundamentally changing our cities and social connections"  
                default_framework = "systems_thinking"
            else:  # Climate Change Ethics
                default_topic = "The ethical responsibilities of individuals and societies in addressing climate change"
                default_framework = "ethical_dimension"
        else:
            default_topic = ""
            default_framework = "human_experience"
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Article Configuration")
        
        # Topic input
        topic = st.text_area("Article Topic:", 
                           value=default_topic,
                           placeholder="Enter your topic or question...",
                           height=100)
        
        # Analysis type selection
        st.subheader("🎚️ Analysis Depth")
        analysis_type = st.radio("Choose analysis depth:",
                               ["🚀 QUICK INSIGHT (3 Layers, 2-3 min)", 
                                "🌳 DEEP ANALYSIS (7 Layers, 8-12 min)"],
                               index=0)
        
        is_quick = "QUICK" in analysis_type
        
        # Philosophical lens selection
        st.subheader("🔍 Philosophical Lens")
        framework_options = {k: v['name'] for k, v in PHILOSOPHICAL_FRAMEWORKS.items()}
        selected_framework = st.selectbox(
            "Choose your philosophical perspective:",
            options=list(framework_options.keys()),
            format_func=lambda x: framework_options[x],
            index=list(framework_options.keys()).index(default_framework) if template != "Custom Topic" else 0
        )
        
        # Display framework info
        if selected_framework:
            framework = PHILOSOPHICAL_FRAMEWORKS[selected_framework]
            with st.expander(f"📚 About {framework['name']}"):
                st.write(f"**Key Thinkers:** {', '.join(framework['thinkers'])}")
                st.write("**Core Questions:**")
                for question in framework['core_questions']:
                    st.write(f"• {question}")
    
    with col2:
        st.header("⚙️ Generation Settings")
        
        # Model selection
        st.subheader("🤖 AI Model")
        model_options = {k: v['name'] for k, v in FREE_MODELS.items()}
        selected_model = st.radio(
            "Choose your AI thinker:",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x]
        )
        
        # Display model info
        model_info = FREE_MODELS[selected_model]
        st.caption(f"**Strengths:** {', '.join(model_info['strengths'])}")
        
        # Tone selection
        st.subheader("🎵 Writing Tone")
        tone = st.select_slider(
            "Adjust the tone:",
            options=["Conversational", "Analytical", "Narrative", "Authoritative"],
            value="Conversational"
        )
        
        # Generation button
        st.markdown("---")
        generate_button = st.button(
            f"🧠 Generate Article",
            type="primary",
            use_container_width=True,
            disabled=not (topic and st.session_state.api_key)
        )
    
    # Philosophical framework display
    if selected_framework:
        framework = PHILOSOPHICAL_FRAMEWORKS[selected_framework]
        st.markdown(f"""
        <div class="philosophy-card" style="border-left-color: {framework['color']}">
            <h4>🎯 Selected Framework: {framework['name']}</h4>
            <p><strong>Guiding Thinkers:</strong> {', '.join(framework['thinkers'])}</p>
            <p><strong>Analysis Depth:</strong> {'3 Layers' if is_quick else '7 Layers'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generation logic
    if generate_button and topic and st.session_state.api_key:
        writer = PhilosophicalWriter()
        
        # Construct prompt based on analysis type
        if is_quick:
            prompt = writer.construct_quick_insight_prompt(topic, selected_framework, tone)
            layer_count = 3
            expected_time = "2-3 minutes"
        else:
            prompt = writer.construct_deep_analysis_prompt(topic, selected_framework, tone)
            layer_count = 7
            expected_time = "8-12 minutes"
        
        # Display generation status
        with st.status(f"🧠 Generating {layer_count}-Layer Philosophical Analysis...", expanded=True) as status:
            st.write("✓ Philosophical framework initialized")
            st.write(f"✓ {framework['name']} lens applied")
            st.write(f"✓ {model_info['name']} model engaged")
            st.write("✓ Building narrative foundation...")
            st.write("✓ Applying philosophical insights...")
            st.write("✓ Synthesizing actionable conclusions...")
            
            # Actual API call
            start_time = time.time()
            article, error = writer.generate_article(
                st.session_state.api_key,
                model_info['id'],
                prompt,
                "deep" if not is_quick else "quick"
            )
            end_time = time.time()
            
            if article:
                st.session_state.generated_article = article
                st.session_state.generation_metrics = {
                    "time_taken": round(end_time - start_time, 2),
                    "model_used": model_info['name'],
                    "framework_used": framework['name'],
                    "analysis_depth": layer_count,
                    "word_count": len(article.split())
                }
                status.update(label="✅ Analysis Complete!", state="complete")
            else:
                st.error(f"❌ Generation failed: {error}")
                status.update(label="❌ Generation Failed", state="error")
    
    # Display generated article
    if st.session_state.generated_article:
        st.markdown("---")
        st.header("📖 Generated Article")
        
        # Metrics
        metrics = st.session_state.generation_metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Generation Time", f"{metrics['time_taken']}s")
        with col2:
            st.metric("Analysis Depth", f"{metrics['analysis_depth']} Layers")
        with col3:
            st.metric("Word Count", metrics['word_count'])
        with col4:
            st.metric("Philosophical Lens", metrics['framework_used'])
        
        # Article display
        st.markdown(st.session_state.generated_article)
        
        # Download options
        st.markdown("---")
        st.header("💾 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Text download
            article_text = st.session_state.generated_article
            st.download_button(
                label="📥 Download as Text",
                data=article_text,
                file_name=f"philosophical_article_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Markdown download
            md_content = f"""# Philosophical Analysis: {topic}

## Framework: {metrics['framework_used']}
## Model: {metrics['model_used']}
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{article_text}
"""
            st.download_button(
                label="📄 Download as Markdown", 
                data=md_content,
                file_name=f"philosophical_article_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # New generation button
        if st.button("🔄 Generate New Article", use_container_width=True):
            st.session_state.generated_article = None
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with Streamlit & Philosophical AI | Free AI Models via OpenRouter</p>
            <p>Age 14+ | Philosophical AI Journalism | Making complex ideas accessible</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()