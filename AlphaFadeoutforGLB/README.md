### 개요

Blender에서 glb 파일 포맷으로 export 할 때, Material 관련 애니메이션은 사용할 수 없다. 예전부터 제기되어 왔던 주제인데 아직 적용되지 않고 있는 듯 하다.

Material 애니메이션 중에 가장 잘 쓸 수 있는 부분은 Alpha FadeOut 효과로, 특정 오브젝트를 투명하게 서서히 사라지게 만든다. glb/gltf 포맷에서도 마찬가지로 사용하기 위해서는 조금의 트릭이 필요하다.

Alpha Fadeout을 적용하고 싶은 오브젝트를 **프레임 단위로 복제하여 각각에 다른 Alpha 값을 부여하면 된다**. 오브젝트를 복제한다는 것이 복잡한 오브젝트에 대해서는 **꽤나 부하를 가져올 것 같은 생각이 든다**. 이 부분에 대해서 Collection Instance를 테스트로 적용해보았지만 결국 오브젝트마다 다른 Alpha를 적용하기 위해서는 일반적인 Duplicate Object 방식으로 진행해야 한다는 부분을 경험했다.

---

## AlphaFadeout 오브젝트 복제 스크립트 (AlphaFadeout.py)

최상단의 Num 변수에 복제할 만큼의 수를 넣는다. 이후 복제하고자 하는 오브젝트를 선택한 후 스크립트를 실행한다. 선택한 기준 오브젝트의 메테리얼은 Alpha Blend가 되고 Backface Culling 옵션도 활성화했다. 이후 Num 변수 크기만큼 오브젝트가 복제되고 Num의 개수에 따라서 Alpha 값이 점점 작아진다. 예를 들어 Num이 10이면 Alpha 값은 0.1씩, Num이 20이면 Alpha 값은 0.05씩 줄어들게 된다. 마지막에 Alpha가 0이 될 때까지.

---

### 사용 방법

- 오브젝트를 하나 생성하고 원하는 메테리얼을 적용한다.

![](https://blog.kakaocdn.net/dn/lOVq5/btsJNY43zCC/yJL1KVQOK6iZKLDnjq7w40/img.png)

- 오브젝트를 선택한 후 스크립트를 실행하면 오브젝트가 복제된다.

![](https://blog.kakaocdn.net/dn/coKpg1/btsJNgMeDEj/rYPTaoxuT73AkuIwIN3DOk/img.png)

---
---

## Particle System 생성 스크립트 (AlphaParticle.py)

최상단 num_particle_systems 변수에는 복제한 오브젝트 만큼의 수에 1을 더한 값을 넣는다.
object_name_base 변수에는 복제할 기준 오브젝트의 이름을 큰따옴표를 이용하여 string 형태로 입력한다.

### 사용 방법

Emitter가 될 오브젝트를 하나 만든다. Plane 생성

![](https://blog.kakaocdn.net/dn/XuxM4/btsJN9yzeP7/3JuDDP5Ei8c1pkm2WqkPvK/img.png)

Emitter가 될 오브젝트를 선택한 후 스크립트를 실행하면 Particle System이 생성되는 것을 볼 수 있다.

![](https://blog.kakaocdn.net/dn/yDreb/btsJOkNz4jr/4hq69hgHc49PGoZW38CtzK/img.png)

이미 각 프레임마다 Alpha 값이 설정된 상태이기 때문에 Timeline을 실행하면 Alpha 애니메이션이 잘 작동하는 것을 볼 수 있다.

![](https://blog.kakaocdn.net/dn/HoJvp/btsJOYb2IMV/6gLuhLwpOoqxw3K4PNU1g0/img.gif)

---

## glb 포맷으로 Export

이제 Govie Tools를 이용해서 각 프레임마다 생성되는 Particle을 export 하면 된다.

export 과정은 이전 글에 썼던 내용과 완전히 동일하기 때문에 참고하면 된다.
https://lightbakery.tistory.com/291