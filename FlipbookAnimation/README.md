## 개요

glb 파일로 이펙트를 export 하는 방법 중 하나는 Flipbook 형태로 이루어져있는 Texture를 이용하는 것이다. 하나의 Texture 이미지 안에 순차적인 움직임이 들어있는 이미지를 각각의 Plane에 적용하여 연속된 하나의 애니메이션으로 표현할 수 있는 것이다.

이 과정에서 각각의 Plane을 생성하여 UV 좌표를 수동으로 수정하는 것에 대한 시간과 노력을 줄이기 위해서 자동화된 스크립트를 시도하게 되었다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/04249748-0d66-40e4-bf80-dbdf8ab31acb/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/2f858430-1e38-42fc-9e6e-8af36f7245eb/image.png)

---

## UV Offset 스크립트 (UVOffset.py)

결론적으로는 완전 자동화된 스크립트를 구현하지 못했다. 복제된 Plane이 이전 UV 데이터를 따라가서 스크립트 실행 후 모든 Plane이 같은 UV를 가지고 있는 형식으로 결과가 나왔기 때문.

위의 스크립트는 **한 번 실행 시 하나의 Plane을 복제하여 UV를 한 칸 옮기는 스크립트**이다. 따라서 UV에 들어있는 이펙트의 개수만큼 실행을 해야한다.

---

## 사용 방법

- Plane을 하나 생성하여 잘 볼 수 있도록 X축 기준 90도 회전했다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/b194198e-c9d5-4a4c-a52b-84c55dcbb91e/image.png)

- Material과 Flipbook 텍스쳐를 적용한다. BaseColor와 Alpha를 잘 연결하고 Material 속성에서 [Alpha Blend] 설정.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/4eb54595-e130-4cd9-b221-71041ba8f77d/image.png)

- UV Editing 모드에서 Text Editor 창을 열어서 스크립트를 넣는다.
이 때, Plane의 UV는 텍스쳐 전체를 덮고 있어야 한다. 가끔 UV unwrap을 하면 텍스쳐의 일부만 덮는 경우가 있는데, 이 경우에는 Unwrap 후 [Correct Aspect]를 체크 해제하면 된다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/23206deb-1f16-4f53-91e7-f95f5f0dc172/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/88269f51-8335-4004-a9a3-41f07e794511/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/9dac7a80-f3b5-4a61-bac2-bc93aab3ef5b/image.png)

- 첫 Plane에 대한 UV 스케일을 맞춘다.
16x4 텍스쳐 기준
Scale X = 1/16
Scale Y = 1/4

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/3d02d91c-5af0-4b69-8e9c-7504c3b0d32f/image.png)

- 첫 Plane에 대한 UV 좌표를 맞춘다.
16x4 텍스쳐 기준, 왼쪽 위 애니메이션 시작 기준
X = 1/32
Y = 1/8*7 (8로 나누고 7을 곱하는 이유는 아래 그림과 같다. UV의 Center Pivot이 해당 줄에 위치해야 하기 때문. x를 32로 나누는 이유도 Center Pivot 때문)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/24b45bfe-a991-4c23-8fc1-834808e37ba4/image.png)

- 기준 Plane을 복제한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/0322951b-2930-41e2-a3c9-4ce63bc9640e/image.png)

- 스크립트를 Column수 - 1 만큼 실행한다.(실행 버튼을 15번 누른다.)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/c77fb895-cf1c-4e74-8c65-a983aa1c5265/image.png)

- 맨 마지막 Mesh가 겹쳐있기 때문에 맨 마지막 Mesh를 지운다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/7933a615-a755-4658-b5bb-b8c0a9e068cb/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/16cc074a-4e83-4eab-a319-b494540f5c12/image.png)

- 기준이 되는 가장 처음 Plane을 다시 복제한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/94ccc0f8-6a3d-40fd-a98e-681963e9e4d2/image.png)

- 스크립트 8번째 줄은 주석처리, 9번째 줄을 활성화 후 스크립트를 실행하여 행을 바꾼다.

```python
#Switch column and row offsets
#offset = Vector((1/column, 0))
offset = Vector((0, -1/row)) #UV의 아래방향으로 가기 위해서 마이너스
```

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/5f6994d1-9399-4c18-93ab-725b430643a5/image.png)

- 이번에는 Plane을 복제하지 않고 그대로 8번째 줄을 활성화 하여 Column - 1 수만큼 스크립트를 실행한다.(15번 실행)

```python
#Switch column and row offsets
offset = Vector((1/column, 0))
#offset = Vector((0, -1/row))
```

- 마찬가지로 맨 마지막 Mesh는 지운다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/ab08c977-8b01-4e73-9363-3144365d8010/image.png)

- 두 번째 줄의 맨 앞 Mesh를 복제하여 다시 행을 바꾸고 반복한다.

```python
#Switch column and row offsets
#offset = Vector((1/column, 0))
offset = Vector((0, -1/row)) #UV의 아래방향으로 가기 위해서 마이너스
```

```python
#Switch column and row offsets
offset = Vector((1/column, 0))
#offset = Vector((0, -1/row))
```

- 잘 수행했다면 Flipbook 텍스쳐 전체를 덮는 모든 Plane을 볼 수 있다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/4c48ac76-3ded-4e86-9cfa-78743347566d/image.png)

---

## Particle System 생성 스크립트 (ParticleSystem.py)

각 Plane이 하나의 텍스쳐 Motion을 가지고 있다면 이제 이 Plane들을 한 프레임마다 하나씩 보여지게 해서 연속된 애니메이션으로 만들어야 한다. Particle System을 사용하면 매 프레임마다 Plane을 하나씩 생성시켜서 목적을 달성할 수 있다.

가장 위 num_particle_systems의 변수에는 Filpbook에 있는 이미지 개수를 넣는다. 16x4 텍스쳐 기준으로 64를 입력한다. 각 이미지를 가지고 있는 Plane을 배열로 저장하고, Particle System을 생성하여 설정을 세팅한다.

여기서 Plane의 이름은 가장 처음의 “Plane”을 포함하여 이후로 “Plane.001”, “Plane.002”, “Plane.003”… 의 규칙성을 가져야 한다. 이름으로 배열을 저장하기 때문.

---

## 사용 방법

- 파티클 시스템을 적용할 오브젝트를 하나 생성한다. (예시로 Plane을 하나 생성하여 이름은 “Emitter”로 바꾸었다. 구분하기 쉽게 Collection 바깥에 위치시켰다.)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/02b0eea7-a2e8-4eb1-b7e4-5f99fa206919/image.png)

- 스크립트 최상단에 num_particle_systems 변수에 Flipbook 이미지 개수를 설정한다.

```python
# Number of particle systems you want to create
num_particle_systems = 64
```

- Emitter가 될 오브젝트를 선택한 후 스크립트를 실행한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/f81e80c8-de1d-4518-8de7-9381f5c492da/image.png)

- Timeline의 마지막 프레임을 마지막 파티클의 수로 설정 후 실행하면 이미지 애니메이션이 자연스럽게 움직이는 것을 볼 수 있다!
    
    ![녹화_2024_09_24_15_59_26_247.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/40e57690-2fb9-4cc2-b425-31b290168b0b/%EB%85%B9%ED%99%94_2024_09_24_15_59_26_247.gif)
    

---

## glb 포맷으로 Export

이후 해당 Flipbook 애니메이션을 glb로 추출하는 방법은 아래의 글에서 찾아볼 수 있는데 확실하게 정리하기 위해서 export 하는 방법을 아래에 다시 기술해야겠다.

[[Blender] 파티클을 glb/gltf로 export 하기](https://lightbakery.tistory.com/245)

Govie Tools를 받았다면 단축키 ‘N’을 눌렀을 때 우측 탭에서 볼 수 있다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/39a70fe6-195f-46b9-9aec-d19cfcdf5cf8/image.png)

Particle Systems가 들어있는 Emitter를 누른 후 Key Visibility를 체크하고 Collection 이름을 설정한 후 [Bake Particles]를 눌러 애니메이션을 Bake 한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/d18c1b49-f48e-45be-918c-a6c058160fc2/image.png)

Bake 된 오브젝트를 모두 선택 한 후 Graph Editor 창으로 이동한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/f36b3a97-2bf7-4f0a-aec2-4a036846965a/image.png)

Outliner 창에서 Plane을 모두 선택 또는 Graph Editor 창에서 단축키 ‘A’를 눌러서 그래프를 모두 선택한 후 마우스 우클릭하여 [Interpolation Mode] - [Constant]로 바꾼다. 이 과정을 거쳐야 glb로 export 했을 때 애니메이션이 제대로 나온다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/79363e82-68f5-41e9-8f49-e8efc62817b1/image.png)

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/d23ac9cf-7fea-4103-88fb-9e73d8b45900/image.png)

추가로, 그래프 상에서는 Scale이 0에서 1로 바뀌고 다시 0으로 작아지는 것 처럼 보이지만 자세히 보면 작아진 상태의 Scale은 0이 아니라 0.01인 것을 볼 수 있다. 

마치 점처럼 작게 가운데에 계속해서 보여지게 된다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/ed2f498a-55d8-4513-bea2-337b9bfd9dc4/image.png)

![녹화_2024_09_24_16_34_46_144.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/612ffbcb-0013-4b50-bf4e-1f36f9f61718/%EB%85%B9%ED%99%94_2024_09_24_16_34_46_144.gif)

이를 해결하기 위하여 Graph Editor에서 scale 값만 검색하여 단축키 ‘A’를 눌러 전체 선택 후 단축키 ‘G’키, ‘Y’키, ‘-0.01’을 입력하여 Y축으로 0.01만큼 내려주면 작아졌을 때의 크기가 0이 되어 점처럼 보이지 않게 할 수 있다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/8584ca56-c1a0-4017-ba82-150d49e0794c/image.png)

이제 export를 위해서 Govie Tools 설정을 바꾼다. [Export Settings] - [Animation]에서 [Group by NLA]로 설정되어 있는 부분을 [Optimize Animation]으로 바꾼 후 추출할 파일 이름을 설정한 후 [Export] 버튼을 눌러서 Export 한다.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/62243bc4-1209-4b93-9c6c-4f4b4ccc4225/image.png)

glb export 완료

![녹화_2024_09_24_16_40_04_898.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/c3357a23-9a22-41fd-84f8-0e4e54c69c28/a65cf165-c0da-40bb-bb46-7e59221737b2/%EB%85%B9%ED%99%94_2024_09_24_16_40_04_898.gif)