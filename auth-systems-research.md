# Enterprise Open Source Authentication & Authorization Systems Research

## Executive Summary

After researching enterprise-grade open source authentication systems (excluding Authentik per your experience), the top recommendations are:

| Rank | System | Best For | Ease of Use | Enterprise Grade |
|------|--------|----------|-------------|------------------|
| 1 | **ZITADEL** | B2B SaaS, multi-tenancy, cloud-native | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 2 | **Keycloak** | Large enterprises, complex federation | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 3 | **Ory Stack** | Maximum flexibility, microservices | ⭐⭐ | ⭐⭐⭐⭐ |

**Recommendation:** ZITADEL offers the best balance of enterprise features, ease of use, and compliance readiness for multi-region deployments.

---

## Compliance Requirements Summary

### UK Requirements
- **UK GDPR** (Data Protection Act 2018)
- **NCSC Cyber Essentials** - Baseline security controls requiring MFA
- **ISO 27001** - Information security management
- Requirements:
  - MFA mandatory for cloud services and administrative access
  - Password hashing with bcrypt, scrypt, or PBKDF2 (not MD5/SHA1)
  - Least privilege access principles
  - Audit logging of privileged user activity

### USA Requirements
- **SOC 2 Type II** - Service organization controls
- **ISO 27001** - Information security management
- **NIST 800-63** - Digital identity guidelines
- **HIPAA** (if healthcare data)
- Requirements:
  - Strong authentication mechanisms
  - Access control and audit trails
  - Encryption at rest and in transit

### Saudi Arabia Requirements
- **NCA Essential Cybersecurity Controls (ECC)** - Mandatory framework
- **Personal Data Protection Law (PDPL)** - Fully effective since Sept 2024
- **SAMA Cybersecurity Framework** (for financial sector)
- Requirements:
  - MFA mandatory for remote access and privileged accounts
  - Periodic review of user identities and access rights
  - Cross-border data transfer requires SDAIA approval
  - Incident reporting to NCA within specified timeframes
  - Penalties up to SAR 5 million or 5% of annual revenue

---

## Detailed System Analysis

### 1. ZITADEL ⭐ RECOMMENDED

**Overview:**
Modern, cloud-native identity platform built with Go. Single binary deployment with event-sourced architecture. Native multi-tenancy designed from the ground up.

**Strengths:**
- ✅ **Native Multi-Tenancy** - Built for B2B, handles organizations/tenants elegantly
- ✅ **API-First Design** - Modern REST APIs and SDKs
- ✅ **Single Binary** - Simpler deployment than Keycloak or Ory
- ✅ **Built-in Audit Trail** - Long-term audit logging out-of-the-box
- ✅ **ISO 27001 Certified** (company certification)
- ✅ **Self-Hosted Option** - Full control over data sovereignty
- ✅ **MFA Built-in** - TOTP, WebAuthn/Passkeys, OTP
- ✅ **OIDC/OAuth2/SAML** support

**Weaknesses:**
- ⚠️ Documentation criticized by some users
- ⚠️ Smaller community than Keycloak
- ⚠️ Initial setup requires ~3 hours to understand

**Production Requirements:**
- Minimum: 512MB RAM, <1 CPU core for ZITADEL
- Database: ~1 CPU core per 100 req/s, 4GB RAM per core
- HA Setup: 3 nodes with 4 CPU cores and 16GB RAM each
- Supports PostgreSQL (easier) or CockroachDB

**Compliance Fit:**
| Region | Compliance | Notes |
|--------|------------|-------|
| UK | ✅ Good | OIDC compliant, MFA, audit logs, GDPR-ready |
| USA | ✅ Good | SOC2-ready architecture, ISO 27001 certified |
| Saudi Arabia | ✅ Good | Self-host for data sovereignty, MFA, audit logging |

**Resources:**
- GitHub: https://github.com/zitadel/zitadel (20k+ stars)
- Docs: https://zitadel.com/docs
- Production Guide: https://zitadel.com/docs/self-hosting/manage/production

---

### 2. Keycloak

**Overview:**
Industry-standard open source IAM, originally developed by Red Hat. CNCF incubation project since 2023. Java-based, runs on Quarkus.

**Strengths:**
- ✅ **Most Mature** - Longest track record, massive community
- ✅ **CNCF Project** - Strong governance and sustainability
- ✅ **Full Protocol Support** - OIDC, OAuth2, SAML 2.0, LDAP
- ✅ **Enterprise SSO** - Identity brokering, federation
- ✅ **Extensive Customization** - SPI extensibility
- ✅ **Red Hat Support** - Commercial backing available

**Weaknesses:**
- ⚠️ **Operational Complexity** - Requires skilled Java/networking team
- ⚠️ **Scaling Issues** - Not truly stateless, sticky sessions needed
- ⚠️ **Multi-Tenancy Limited** - Historically struggled beyond 100-200 realms (improved in 26.4)
- ⚠️ **Admin UI Overwhelming** - Steep learning curve
- ⚠️ **Documentation Gaps** - Real-world production setups poorly documented

**Known Production Issues:**
- Infinispan cache configuration complexity
- Kubernetes deployment requires careful tuning
- Session management at scale
- Realm scaling (though improved with Organizations feature)

**Compliance Fit:**
| Region | Compliance | Notes |
|--------|------------|-------|
| UK | ✅ Good | Mature, widely audited |
| USA | ✅ Good | Used by many Fortune 500 |
| Saudi Arabia | ✅ Good | Self-hostable, but complex |

**Resources:**
- Site: https://www.keycloak.org
- GitHub: https://github.com/keycloak/keycloak (25k+ stars)
- Production Guide: https://www.keycloak.org/server/configuration-production

---

### 3. Ory Stack (Kratos + Hydra + Keto + Oathkeeper)

**Overview:**
Modular, microservices-based IAM. Each component is purpose-built: Kratos (identity), Hydra (OAuth2), Keto (permissions), Oathkeeper (API gateway).

**Strengths:**
- ✅ **Cloud-Native Architecture** - True microservices
- ✅ **Flexibility** - Pick only components you need
- ✅ **Go-Based** - High performance, low resource usage
- ✅ **Hydra OAuth2** - Fully spec-compliant
- ✅ **Scales to Billions** - Designed for massive scale

**Weaknesses:**
- ⚠️ **Integration Complexity** - Must wire multiple services together
- ⚠️ **Version Management** - Must coordinate 3+ repos
- ⚠️ **Enterprise Features Paywalled** - SAML, SCIM, SSO require Ory Network or Enterprise License
- ⚠️ **Steeper Learning Curve** - Multiple concepts to understand
- ⚠️ **SPA Challenges** - Cookie/session handling can be tricky

**Enterprise License Required For:**
- SAML support
- SCIM provisioning
- Domain-bound SSO
- Enterprise CVE patches with SLA

**Compliance Fit:**
| Region | Compliance | Notes |
|--------|------------|-------|
| UK | ⚠️ Moderate | Requires enterprise license for full compliance |
| USA | ⚠️ Moderate | SOC2/ISO27001 features need enterprise tier |
| Saudi Arabia | ⚠️ Moderate | Self-hostable but complex |

**Resources:**
- Site: https://www.ory.sh
- Kratos: https://github.com/ory/kratos (11k+ stars)
- Hydra: https://github.com/ory/hydra (15k+ stars)

---

## Other Notable Options

### SuperTokens
- Developer-friendly, good for startups
- Less enterprise focus
- Limited SAML support

### Logto
- Modern, developer-first
- SOC2-ready architecture
- Newer, smaller community

### Gluu
- Strong MFA (TOTP, SMS, biometrics)
- Used by universities and enterprises
- More complex setup

### OpenIAM
- Converged IGA/SSO/MFA/CIAM/PAM platform
- Zero-trust focused
- Commercial-first with open source components

---

## Decision Matrix

| Criteria | ZITADEL | Keycloak | Ory |
|----------|---------|----------|-----|
| Ease of Setup | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Ease of Use | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Multi-Tenancy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Documentation | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Community Size | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Enterprise Maturity | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Operational Overhead | Low | High | Medium |
| Data Sovereignty | ✅ | ✅ | ✅ |
| SAML Support | ✅ | ✅ | Enterprise Only |
| SCIM Support | ✅ | ✅ | Enterprise Only |

---

## Recommendations by Use Case

### If you need simplicity + enterprise features:
→ **ZITADEL** - Best balance of features and ease of use

### If you have a dedicated DevOps/Platform team:
→ **Keycloak** - Most mature, but requires operational investment

### If you're building a highly customized microservices architecture:
→ **Ory** - Maximum flexibility, but higher complexity

### For Saudi Arabia data sovereignty requirements:
→ **ZITADEL or Keycloak** self-hosted - Both support on-premise deployment

---

## Implementation Considerations

### For All Regions (UK, USA, Saudi Arabia):

1. **MFA is Mandatory** - All three options support TOTP, WebAuthn
2. **Audit Logging** - ZITADEL has best out-of-box; Keycloak requires configuration
3. **Password Policies** - All support configurable password policies
4. **Encryption** - Ensure TLS everywhere, encryption at rest for database
5. **Data Residency** - Self-host in region-specific infrastructure

### Saudi Arabia Specific:
- Deploy within KSA or ensure SDAIA approval for cross-border transfers
- Implement incident reporting capabilities (NCA requirement)
- Ensure periodic access review capabilities

---

## Sources

- [Cerbos: Best Open Source Auth Tools 2025](https://www.cerbos.dev/blog/best-open-source-auth-tools-and-software-for-enterprises-2025)
- [ZITADEL vs Keycloak Comparison](https://zitadel.com/blog/zitadel-vs-keycloak)
- [House of FOSS: Keycloak vs Zitadel 2025](https://www.houseoffoss.com/post/keycloak-vs-zitadel-which-open-source-identity-provider-should-you-choose-in-2025)
- [Keycloak Production Configuration](https://www.keycloak.org/server/configuration-production)
- [NCSC Identity and Access Management](https://www.ncsc.gov.uk/collection/10-steps/identity-and-access-management)
- [UK ICO Passwords Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/security/a-guide-to-data-security/passwords-in-online-services/)
- [NCA Essential Cybersecurity Controls](https://nca.gov.sa/ecc-en.pdf)
- [Saudi Arabia PDPL Compliance](https://www.wattlecorp.com/saudi-arabia-pdpl-compliance/)
- [Sirius: Problems with Keycloak](https://www.siriusopensource.com/en-us/blog/problems-keycloak-unpacking-challenges)
- [ZITADEL Production Setup](https://zitadel.com/docs/self-hosting/manage/production)
- [Logto: Top 5 OSS IAM Providers 2025](https://blog.logto.io/top-oss-iam-providers-2025)
