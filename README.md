# base-images

docker base images for JupyterHub environment


### Steps for performing update

* [DEPRECATED: will be moved to qhub] Tag new version with preview tag (e.g. `2022.02-preview.0`). Github action will automatically trigger a build
* Execute notebooks with new version via `https://contributions-api.hub.eox.at/notebook-execute-all-active?api_key=${API_KEY}&base_image_tag=${NEW_TAG}`
* If all notebooks executed successfully, copy them to the notebook repo and commit them (e.g. in jupyter environment)
  (make sure that version in notebook output is correct)
* [DEPRECATED] Tag new version in this repo (if the base image is to be updated, tag `base-X` and update `FROM` in user image)
* Release on github.com and add the output of `conda list` as release notes
* Update image version in `flux-config` (mostly `customer-operator` and `contribution-handler`, but simply just grep for old version)
* Also update `IMAGE_TAG_LATEST_BUT_ONE` in `customer-operator` config
* Also update image version in marketplace-handler
* Update notebook bucket:  
  ```
  kubectl -n edc delete -f ~/git/flux-config/workloads/edc/update-notebooks-job.yaml
  kubectl -n edc apply -f ~/git/flux-config/workloads/edc/update-notebooks-job.yaml
  ```
* Cycle relevant services: `contribution-handler`, `nbviewer`, `customer-operator`


