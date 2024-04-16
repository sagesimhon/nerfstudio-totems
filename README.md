As part of my Master’s thesis, an integration of [Totems](https://jingweim.github.io/totems/)[^1] with [Nerfstudio](https://github.com/nerfstudio-project/nerfstudio)[^2] in order to achieve faster radiance field optimization and to examine the versatility of the original Totems implementation.

What I learned: 

Nerfstudio (specifically, the `nerfacto` model) faces challenges in reproducing reconstructions of the unwarped totem rays comparable in quality to the original NeRF implementation due to the large presence of floaters, except for a few higher quality views. 

Additionally, found easily breakable code when modularizing with Nerfstudio and running larger jobs. This revealed the need for future work to develop more robust implementations and integration of these complex, resource-intensive projects and address issues discovered in the rendering backend and job manager summarized [here](https://github.com/mitsuba-renderer/mitsuba3/issues/849), [here](https://github.com/mitsuba-renderer/drjit-core/issues/63), and [here](https://github.com/mitsuba-renderer/mitsuba3/issues/190). 

In light of this and due to the fact that NeRF-based Totems relies on a new optimization for every scene, we ultimately switched to a 2D, generalizable, NeRF-independent, more efficient approach that can be used on any scene within a depth tolerance and with the same totem-camera configuration. This project can be found [here](https://github.com/sagesimhon/totem_plus)

![alt text](https://github.com/sagesimhon/nerfstudio-totems/blob/main/nerstudio.png)

[^1]: Jingwei Ma, Lucy Chai, Minyoung Huh, Tongzhou Wang, Ser-Nam Lim, Phillip Isola, and Antonio Torralba. Totems: Physical objects for verifying visual in- tegrity. ECCV, 2022.
[^2]: Matthew Tancik, Ethan Weber, Evonne Ng, Ruilong Li, Brent Yi, Terrance Wang, Alexander Kristoffersen, Jake Austin, Kamyar Salahi, Abhik Ahuja, David Mcallister, Justin Kerr, and Angjoo Kanazawa. Nerfstudio: A modu- lar framework for neural radiance field development. In Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Pro- ceedings, SIGGRAPH ’23. ACM, July 2023.

