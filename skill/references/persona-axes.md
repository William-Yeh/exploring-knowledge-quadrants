# Persona Axes Reference

Use this reference in deep mode to select two orthogonal axis types for
persona generation. Personas at the intersection of two different axis types
are structurally non-redundant — they see different blind spots.

## Axis Types

### Domain Dimension (STEEP)

| Label | Focus |
|-------|-------|
| Social | Human behavior, culture, communities, ethics |
| Technological | Tools, systems, technical constraints |
| Economic | Cost, incentives, markets, resource flows |
| Environmental | Physical environment, sustainability, externalities |
| Political | Power, policy, regulation, governance |
| Legal | Law, liability, compliance, intellectual property |

### System Position (CATWOE-inspired)

_Derived from CATWOE with additions (Competitor, Maintainer) for adversarial and long-term scenarios._

| Label | Focus |
|-------|-------|
| Customer / End User | Who receives value from the system |
| Actor / Creator | Who builds or operates the system |
| Owner | Who is accountable for the system |
| Regulator | Who sets rules the system must follow |
| Competitor | Who builds alternatives or benefits from failure |
| Maintainer / Inheritor | Who lives with the system long-term |

### Temporal Horizon

| Label | Focus |
|-------|-------|
| Operational | Days to weeks — immediate execution concerns |
| Strategic | Months to 1–3 years — planning and adaptation |
| Systemic | Decade+ — civilizational, path-dependency concerns |

### Adversarial Triad

| Label | Focus |
|-------|-------|
| Attacker | Wants the effort to fail — adversarial, exploit-focused |
| Regulator | Holds the effort accountable — compliance, accountability |
| Inheritor | Has to live with outcomes long-term — maintenance, technical debt |

## Selecting Axes

Choose two axes from **different** types. Good pairs:

| Pair | Example persona generated |
|------|--------------------------|
| STEEP × CATWOE | Economic × Regulator → economist who evaluates regulatory incentives |
| STEEP × Adversarial | Social × Attacker → social-engineering threat analyst |
| CATWOE × Temporal | End User × Systemic → researcher studying decade-long user behavior shifts |
| STEEP × Temporal | Technological × Strategic → CTO planning 2-year technology bets |

Avoid pairing axes of the **same type** (e.g., Social × Economic, or
Operational × Strategic) — personas will overlap in what they see.
