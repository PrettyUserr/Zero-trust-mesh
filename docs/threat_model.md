## Threat Model — Zero Trust Service Mesh

Author: Ibukun Olaniyan
Date: 10th June, 2026.
Version: 1.0
Framework: NIST SP 800-207 Zero Trust Architecture


# 1. Problem statement:

Without zero trust controls, a single compromised pod in a Kubernetes cluster gives an attacker free movement to every other pod in the cluster.This means: No authentication, no encryption and no restrictions. One vulnerability becomes a full compromise.

This project implements zero trust principles at the network layer. Every service must prove its identity before communicating with any other service, and all traffic is encrypted end to end.

# 2. What are we building?

Three microservices running in a Kubernetes cluster:
- frontend — accepts user requests, talks only to backend
- backend — processes requests, talks only to database
- database — stores data, accepts connections only from backend

Zero trust controls applied:
- Network Policies — whitelist-only traffic rules between pods
- Istio service mesh — automatic mTLS for all service-to-service communication
- Namespace isolation — each service in its own namespace


# 3. NIST SP 800-207 Zero Trust Principles applied

Principle -- How this project implements it 

 All communication is authenticated -- mTLS — both sides present certificates 
 Access is granted on a per-session basis -- Network Policies evaluated per connection 
 Access to resources is determined by dynamic policy -- Istio AuthorizationPolicy per service 
 The enterprise monitors and validates all traffic -- Istio telemetry and access logs 
 No implicit trust based on network location -- Pods in same namespace still require authentication 


# 4. Assets

Asset -- Impact if compromised 

 Frontend pod: Entry point for user traffic -- if compromised, attacker gains foothold
 Backend pod: Business logic -- contains application secrets and data processing 
 Database pod: Crown jewel -- contains all stored data 
 Service mesh certificates -- If stolen, attacker can impersonate any service 
 Kubernetes API server -- Full cluster control if compromised 


# 5. STRIDE Analysis

Threat | Example in this project 

 Spoofing | Malicious pod impersonates backend to access database directly 
 Tampering | Attacker intercepts unencrypted pod-to-pod traffic and modifies it 
 Repudiation | No record of which service made which API call 
 Information Disclosure | Unencrypted traffic between pods exposes sensitive data 
 Denial of Service | Compromised pod floods internal services with requests 
 Elevation of Privilege | Frontend pod gains direct database access it should never have 


# 6. Attack surface — before zero trust controls

Vector | Risk | Likelihood 

 Any pod talking to any pod | Full lateral movement | High 
 Unencrypted pod-to-pod traffic | Data interception | Medium 
 No service identity verification | Spoofing attacks | Medium 
 Flat namespace | No blast radius containment | High 


# 7. Attack surface — after zero trust controls

| Vector | Residual Risk | Control applied 

 Frontend to database direct | Eliminated | Network Policy blocks it 
 Unencrypted traffic | Eliminated | mTLS encrypts all traffic 
 Service impersonation | Low | Istio certificates verify identity 
 Lateral movement post-compromise | Low | Blast radius contained to one namespace 


# 8. Limitations

- mTLS protects traffic between services but not traffic entering the cluster from outside
- A compromised Kubernetes API server bypasses all controls
- Network Policies do not inspect payload content — only source and destination
- Certificate rotation must be managed — expired certificates break service communication
- This is a single-node minikube cluster — production would require multi-node hardening


## 9. References

- NIST SP 800-207 Zero Trust Architecture
  https://csrc.nist.gov/publications/detail/sp/800-207/final
- Kubernetes Network Policies
  https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Istio Security Documentation
  https://istio.io/latest/docs/concepts/security/
- MITRE ATT&CK — Lateral Movement
  https://attack.mitre.org/tactics/TA0008/