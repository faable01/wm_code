package java_mistakes;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BegginerMistakes {
    public static void main(String[] args) {
        useAsList();
        useSubList();
        useAnonymousAndInitializer();
        raiseConcurrentModificationException();
    }

    /** Arrays.asListは固定長 */
    private static void useAsList() {
        List<String> l = Arrays.asList("foo", "hoo");
        try {
            l.add("hoge");
        } catch(Exception e) {
            System.out.println(e);
            // 出力：java.lang.UnsupportedOperationException
        }
    }

    /** Arrays.subListは参照としてリストを抜き出す（のでaddすると元の配列にも要素が追加される） */
    private static void useSubList() {
        List<String> l = new ArrayList<>(Arrays.asList("1", "2", "3", "4", "5"));
        List<String> sl = l.subList(2, 4);

        System.out.println("初期リスト：" + l);
        System.out.println("subListで抜き出したリスト：" + sl);

        sl.add("hoge");

        System.out.println("hoge追加後の「subListで抜き出したリスト」：" + sl);
        System.out.println("hoge追加後の初期リスト：" + l);
        /**
         * ### 出力結果
         * 初期リスト：[1, 2, 3, 4, 5]
         * subListで抜き出したリスト：[3, 4]
         * hoge追加後の「subListで抜き出したリスト」：[3, 4, hoge]
         * hoge追加後の初期リスト：[1, 2, 3, 4, hoge, 5]
         */
    }

    /** コンストラクタの後の括弧は匿名関数とかインスタンスイニシャライザとか */
    private static void useAnonymousAndInitializer() {
        List<String> l = new ArrayList<String>(){
            private static final long serialVersionUID = 1L;
            {
                this.add("foo");
                this.add("hoo");
            }
        };
        System.out.println(l);
        // 出力：[foo, hoo]
        // ▲ インスタンス作った時点ですぐに要素が追加されている
    }

    /** オブジェクトの並行変更を検出すると発生する例外（リストの繰り返し処理中などで起きがち） */
    private static void raiseConcurrentModificationException() {

        // ## 例外パターン1（サブリスト作成後に元配列に要素追加）
        List<String> list1_ng = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        List<String> sl = list1_ng.subList(1, 2);
        list1_ng.add("foooooo");
        System.out.println(list1_ng);  // [foo, hoo, hoge, foooooo]
        try {
            System.out.println(sl);
        } catch(Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }

        // ## 例外にならないパターン1（サブリスト作成前にadd）
        List<String> list1_ok = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        list1_ok.add("foooooo");  // 
        List<String> sli = list1_ng.subList(1, 2);
        System.out.println(list1_ok);  // [foo, hoo, hoge, foooooo]
        System.out.println(sli);  // [hoge]

        // ## 例外パターン2（繰り返し処理中の要素番号の変更（番号をひとつ前に詰める））
        List<String> list2_ng = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        try {
            for (String str : list2_ng) {
                if ("foo".equals(str)) {
                    list2_ng.remove(str);
                }
            }
        } catch (Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }
        System.out.println(list1_ng);  // [hoo, hoge]
        // （エラー出てもキャッチすれば要素操作の実行自体はされている）

        // ## 例外にならないパターン2（要素番号の変更処理のあと、配列のループが存在しない）
        // [foo, hoo, hoge]
        List<String> list2_ok = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        for (String str : list2_ok) {
            System.out.println("走査対象：" + str);
            if ("hoo".equals(str)) {
                list2_ok.remove(str);
            }
        }
        System.out.println(list2_ok);
        /**
         * ### 出力
         * 走査対象：foo
         * 走査対象：hoo
         * [foo, hoge]
         */

        // ## 例外パターン3（繰り返し処理中の要素番号の変更（末尾の番号を増やす））
        List<String> list3_ng = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        try {
            for (String str : list3_ng) {
                list3_ng.add(str);
                if ("hoge".equals(str)) {
                    break;
                }
            }   
        } catch (Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }
        System.out.println(list3_ng);  // [foo, hoo, hoge, foo]
        
        // ## パターン3はどの要素番号でaddしようと繰り返し処理との兼ね合いでアウト
        List<String> list3_ng2 = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        try {
            for (String str : list3_ng2) {
                if ("hoge".equals(str)) {
                    list3_ng2.add(str);
                }
            }   
        } catch (Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }
        System.out.println(list3_ng2);  // [foo, hoo, hoge, hoge]
    }
}