# ToyProject - ALD

## ABSTRACT

 이 프로젝트에서는 구매할 책들의 ISBN을 입력했을 때, 한국의 온-오프라인 서점 알라딘에서 구매할 수 있는 최저가를 도출한다. 

 알라딘은 새 책을 판매할 뿐만 아니라 중고책들도 훼손의 정도에 따라 가격을 차등하여 판매하고 있다.
이렇게 소비자에게 넓은 선택의 폭을 제공하는 것은 알라딘 만의 큰 장점이나, 선택할 수 있는 옵션이 여러가지인 만큼 옵션 중 최저가인 옵션을 알아내는 일은 수고스러운 일이 된다. 

 예를 들어, {'책_ㄱ' : {'직배송':15000, '뉴욕점':13000, '파리점':14000}, '책_ㄴ' : {'파리점':6000, '서울점':5000}}의 딕셔너리가 있다고 가정해보자.
소비자가 '책_ㄱ', '책_ㄴ'을 구매하려 할 때 선택할 수 있는 옵션은 총 3*2가지 이다. 
이 옵션 중 단순히 책의 가격만 생각하여 최저가를 구한다면 각 책마다의 최저가인 뉴욕점에서 '책_ㄱ', 서울점에서 '책_ㄴ'을 구매하여 18,000원이 지출비용이겠으나 매장마다 총 비용이 20,000원이 넘지 않는다면 각 매장마다 2,500원의 배송료가 붙으므로 총 비용은 23,000원이 된다.
하지만 파리점 한 곳에서 '책_ㄱ','책_ㄴ'을 구매한다면 배송비 0원에 총 비용 20,000원으로 책 각각의 최저가를 선택하여 구매하는 것 보다 3,000원 저렴하고, 높아진 각각의 책 가격만큼 책 컨디션도 보다 좋을 것으로 기대할 수 있다. 

 가격만을 고려하는 본인같은 소비자를 위하여 구매할 책의 리스트를 인풋한다면 알라딘에서 구매할 수 있는 최저가 옵션을 출력하도록 프로그램을 구성하였다.


---

## MANUAL

1. 사고 싶은 책들의 ISBN을 찾아본다.
2. 작성예정~~~~~~~~~~~~~~~~~~~~~~~~

### 알라딘 홈페이지에서 ISBN찾는 법

1. 사고싶은 책을 검색한다.
2. 살 책의 새책 페이지에 들어간다.
 
![image](https://github.com/uoahy-6uoas/proj-ALD/assets/144662602/9edbcbfc-c987-4ee4-92a2-e7fdf6bc48d1)

Ta-Da

---


## robots.txt

[CHECK](https://www.aladin.co.kr/robots.txt) Aladin's robots.txt

### User-agent: *
* Disallow: /mobile/
* Disallow: /js/
* Disallow: /aaintraweb/
* Disallow: /account/
* Disallow: /api/
* Disallow: /errormng/
* Disallow: /intranet/
* Disallow: /jiny/
* Disallow: /login/
* Disallow: /mail/
* Disallow: /mng/
* Disallow: /order/
* Disallow: /scm/
* Disallow: /search/
* Disallow: /ttb/
* Disallow: /webservice/
* Disallow: /wservice/
* Disallow: /*?EventId=201357
* Disallow: /*?EventId=199338
* Disallow: /*?EventId=198631
* Disallow: /shop/book/wletslookViewerNew.aspx
* Disallow: /*.swf$
* Allow: /
  
### User-Agent: QuerySeekerSpider ( http://queryseeker.com/bot.html )
* Disallow: /

### User-agent: AhrefsBot
* Disallow: /
  
### User-agent: MJ12bot
* Disallow: /
  
### User-agent: SemrushBot
* Disallow: /

### User-agent: Baiduspider
* Disallow: /
  
### User-agent: Ezooms
* Disallow: /
  
### User-agent: YandexBot
* Disallow: /
  
### User-agent: ltx71
* Disallow: /
  
### User-agent: zgrab/0.x
* Disallow: /

Sitemap: https://www.aladin.co.kr/ucl_editor/util/sitemap/sitemap.xml

---

## Role
 ///////    //      //     //////        ///       /////////
//          //      //   //      //     // //    //
////////    //      //   //      //    //   //   //////////
//    //    //      //   //      //   /////////          //
//    //     //    //    //      //  //      //         // 
///////        ////        //////    //      //  ////////

aladin.robots.txt에서 허락한 /shop/UsedShop 을 사용하도록 한다.
