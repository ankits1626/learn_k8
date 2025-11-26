# Kubernetes Learning Journey - Checkpoint Roadmap

## 🎯 Your Learning Path

This roadmap breaks down the full Kubernetes tutorial into manageable checkpoints. Each checkpoint is a separate file with theory, hands-on exercises, and concept checks.

**Progress Tracking:**
- ⏳ Not Started
- 🔄 In Progress
- ✅ Completed

---

## Checkpoint Structure

### **Checkpoint 0: Foundation Setup** ⏳
**File:** `checkpoint_00_setup.md`
**Time:** 15-20 minutes
**Goals:**
- Verify all tools are installed
- Understand what each tool does
- Get comfortable with terminal commands
- Quick start: Launch your first minikube cluster

**Key Concepts:** Docker, kubectl, minikube, k9s

---

### **Checkpoint 1: Containers Before Kubernetes** ⏳
**File:** `checkpoint_01_containers.md`
**Time:** 30-45 minutes
**Goals:**
- Create a simple Python Flask web app
- Build Docker images
- Run containers locally
- Understand why we need orchestration

**Key Concepts:** Containers, Images, Dockerfile, Ports, Environment Variables

**Hands-on:**
- Write a Flask app
- Build Docker image
- Run multiple versions of containers
- Expose different ports

---

### **Checkpoint 2: Your First Kubernetes Pod** ⏳
**File:** `checkpoint_02_pods.md`
**Time:** 30-45 minutes
**Goals:**
- Start minikube cluster
- Deploy your first pod
- Access the pod
- View logs and debug
- Understand pod lifecycle

**Key Concepts:** Cluster, Node, Pod, kubectl, YAML manifests

**Hands-on:**
- Start minikube
- Write pod.yaml
- Deploy to cluster
- Port-forward to access
- Execute commands inside pod

---

### **Checkpoint 3: Deployments & Self-Healing** ⏳
**File:** `checkpoint_03_deployments.md`
**Time:** 45-60 minutes
**Goals:**
- Understand why Deployments > Pods
- Create deployments with multiple replicas
- See self-healing in action
- Perform rolling updates
- Rollback changes

**Key Concepts:** Deployment, ReplicaSet, Replicas, Rolling Updates, Rollback

**Hands-on:**
- Create deployment with 3 replicas
- Delete a pod and watch it recreate
- Scale up/down
- Update to v2 with zero downtime
- Rollback to v1

---

### **Checkpoint 4: Services & Networking** ⏳
**File:** `checkpoint_04_services.md`
**Time:** 45-60 minutes
**Goals:**
- Understand pod networking challenges
- Create stable endpoints with Services
- Learn different service types
- Test service discovery with DNS
- Load balance across pods

**Key Concepts:** Service, ClusterIP, NodePort, LoadBalancer, DNS, Endpoints

**Hands-on:**
- Create ClusterIP service
- Test internal DNS
- Create NodePort for external access
- Watch load balancing in action

---

### **Checkpoint 5: Configuration Management** ⏳
**File:** `checkpoint_05_config_secrets.md`
**Time:** 30-45 minutes
**Goals:**
- Separate config from code
- Use ConfigMaps for settings
- Use Secrets for sensitive data
- Inject config as env vars and files

**Key Concepts:** ConfigMap, Secret, Environment Variables, Volume Mounts

**Hands-on:**
- Create ConfigMap from literals and YAML
- Create Secrets
- Mount as environment variables
- Mount as files in pods

---

### **Checkpoint 6: Ingress & External Access** ⏳
**File:** `checkpoint_06_ingress.md`
**Time:** 45-60 minutes
**Goals:**
- Understand Ingress vs Service
- Set up nginx Ingress controller
- Configure host-based routing
- Configure path-based routing
- Test with local DNS

**Key Concepts:** Ingress, Ingress Controller, Routing Rules, Annotations

**Hands-on:**
- Enable minikube ingress addon
- Create ingress for multiple hosts
- Set up path-based routing
- Configure /etc/hosts for local testing

---

### **Checkpoint 7: Namespaces & Environments** ⏳
**File:** `checkpoint_07_namespaces.md`
**Time:** 30-45 minutes
**Goals:**
- Understand namespace isolation
- Create dev/prod environments
- Deploy same app to different namespaces
- Cross-namespace communication
- Resource quotas

**Key Concepts:** Namespace, Resource Quotas, Context, FQDN

**Hands-on:**
- Create dev and prod namespaces
- Deploy to both environments
- Test cross-namespace DNS
- Set resource quotas

---

### **Checkpoint 8: Auto-Scaling** ⏳
**File:** `checkpoint_08_autoscaling.md`
**Time:** 45-60 minutes
**Goals:**
- Understand resource requests/limits
- Set up Horizontal Pod Autoscaler (HPA)
- Generate load to trigger scaling
- Watch auto-scaling in action
- Understand scale-up and scale-down behavior

**Key Concepts:** HPA, Metrics Server, CPU/Memory Utilization, Requests vs Limits

**Hands-on:**
- Set resource requests/limits
- Create HPA
- Generate load with load generator
- Watch pods scale up
- Watch cooldown and scale down

---

### **Checkpoint 9: Helm - Package Manager** ⏳
**File:** `checkpoint_09_helm.md`
**Time:** 60-90 minutes
**Goals:**
- Understand why Helm exists
- Create your first Helm chart
- Use values.yaml for configuration
- Deploy to multiple environments
- Manage releases and rollbacks

**Key Concepts:** Helm Chart, Values, Templates, Release, Repository

**Hands-on:**
- Create helm chart from scratch
- Customize with values.yaml
- Install/upgrade/rollback releases
- Create dev-values.yaml and prod-values.yaml
- Package and share chart

---

### **Checkpoint 10: GitOps with ArgoCD** ⏳
**File:** `checkpoint_10_gitops.md`
**Time:** 60-90 minutes
**Goals:**
- Understand GitOps principles
- Install ArgoCD
- Create Git repository for configs
- Set up automated deployments
- Experience declarative deployment workflow

**Key Concepts:** GitOps, ArgoCD, Sync, Application, Self-Healing

**Hands-on:**
- Install ArgoCD
- Create git repo with app configs
- Create ArgoCD application
- Make changes in git → auto-deploy
- Experience self-healing

---

### **Checkpoint 11: Production Simulation** ⏳
**File:** `checkpoint_11_production_sim.md`
**Time:** 90-120 minutes
**Goals:**
- Deploy auto-approver locally
- Understand production architecture
- Map local setup to EKS production
- Complete end-to-end workflow

**Key Concepts:** Full Stack, Production Architecture, CI/CD Pipeline

**Hands-on:**
- Build auto-approver image
- Create production-like Helm values
- Deploy with all components
- Compare to Rewardz EKS setup

---

### **Checkpoint 12: Troubleshooting & Best Practices** ⏳
**File:** `checkpoint_12_troubleshooting.md`
**Time:** 45-60 minutes
**Goals:**
- Learn debugging techniques
- Common issues and solutions
- Best practices for production
- Commands cheatsheet

**Key Concepts:** Debugging, kubectl describe, logs, events

**Hands-on:**
- Intentionally break things
- Debug and fix them
- Practice with k9s
- Build troubleshooting muscle memory

---

## 📊 Recommended Learning Schedule

### **Week 1: Foundations**
- Day 1: Checkpoint 0 + 1 (Setup + Containers)
- Day 2: Checkpoint 2 (Pods)
- Day 3: Checkpoint 3 (Deployments)
- Day 4: Review + Practice
- Day 5: Checkpoint 4 (Services)

### **Week 2: Advanced Concepts**
- Day 1: Checkpoint 5 (Config/Secrets)
- Day 2: Checkpoint 6 (Ingress)
- Day 3: Checkpoint 7 (Namespaces)
- Day 4: Checkpoint 8 (Auto-scaling)
- Day 5: Review + Practice

### **Week 3: Production Ready**
- Day 1-2: Checkpoint 9 (Helm)
- Day 3-4: Checkpoint 10 (GitOps/ArgoCD)
- Day 5: Review + Practice

### **Week 4: Real-World Application**
- Day 1-2: Checkpoint 11 (Production Simulation)
- Day 3: Checkpoint 12 (Troubleshooting)
- Day 4-5: Personal projects + Experiments

---

## 🎓 Learning Methodology

Each checkpoint follows this structure:

1. **📚 Concepts** - What and Why
2. **🔧 Hands-on Exercises** - Step-by-step tasks
3. **💡 Real-World Connection** - How this applies to Rewardz
4. **✅ Concept Check** - Quick quiz to verify understanding
5. **🚀 Challenge** - Optional advanced exercise
6. **📝 Summary** - Key takeaways

---

## ✨ Coach's Notes

- **Don't rush** - Understanding > Speed
- **Make mistakes** - Break things intentionally to learn
- **Ask questions** - No question is too basic
- **Practice commands** - Muscle memory matters
- **Take breaks** - Learning is a marathon, not a sprint
- **Review regularly** - Revisit previous checkpoints

---

## 📈 Progress Tracker

Update this as you complete each checkpoint:

- [ ] Checkpoint 0: Foundation Setup
- [ ] Checkpoint 1: Containers Before Kubernetes
- [ ] Checkpoint 2: Your First Kubernetes Pod
- [ ] Checkpoint 3: Deployments & Self-Healing
- [ ] Checkpoint 4: Services & Networking
- [ ] Checkpoint 5: Configuration Management
- [ ] Checkpoint 6: Ingress & External Access
- [ ] Checkpoint 7: Namespaces & Environments
- [ ] Checkpoint 8: Auto-Scaling
- [ ] Checkpoint 9: Helm - Package Manager
- [ ] Checkpoint 10: GitOps with ArgoCD
- [ ] Checkpoint 11: Production Simulation
- [ ] Checkpoint 12: Troubleshooting & Best Practices

---

**Ready to start?** Let's begin with Checkpoint 0! 🚀

Your coach will create each checkpoint as you progress, adapting to your learning style and pace.
