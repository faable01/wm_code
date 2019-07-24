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

    private static void raiseConcurrentModificationException() {

        // ## 例外パターン1（サブリスト作成後に元配列に要素追加）
        List<String> l = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        List<String> sl = l.subList(1, 2);
        l.add("foooooo");
        System.out.println(l);  // [foo, hoo, hoge, foooooo]
        try {
            System.out.println(sl);
        } catch(Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }

        // ## 例外パターン2
        try {
            // l: [foo, hoo, hoge, foooooo]
            for (String str : l) {
                if ("foo".equals(str)) {
                    l.remove(str);
                }
            }
        } catch (Exception e) {
            System.out.println(e);
            // 出力：java.util.ConcurrentModificationException
        }
        System.out.println(l);  // [hoo, hoge, foooooo]
        // （エラー出てもキャッチすれば要素操作の実行自体はされている）

        // ## 例外にならないパターン1（サブリスト作成前にadd）
        List<String> li = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        li.add("foooooo");  // 
        List<String> sli = l.subList(1, 2);
        System.out.println(li);  // [foo, hoo, hoge, foooooo]
        System.out.println(sli);  // [hoge]

        // ## 例外にならないパターン2（要素番号の変更処理のあと、配列のループが存在しない）
        // [foo, hoo, hoge, foooooo]
        for (String str : li) {
            System.out.println("走査対象：" + str);
            if ("hoge".equals(str)) {
                li.remove(str);
            }
        }
        System.out.println(li);
        /**
         * ### 出力
         * 走査対象：foo
         * 走査対象：hoo
         * 走査対象：hoge
         * [foo, hoo, foooooo]
         */
    }

}