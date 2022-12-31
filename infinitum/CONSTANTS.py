# for some constant values that a few files use, useful to be wary of circular imports
import re

MBT_SIZE = 1024*1024//2 # 0.5 MB
MFT_SIZE = 1*1024*1024 # 1 MB
BLOCKSIZE = 1024*1024//4 # .25 MB
RESERVED_SPACE = MBT_SIZE + MFT_SIZE

Pattern_TextHandler = re.compile(r'(\n|[^\s]+)|(?: ( +) )')
Pattern_Password = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\d\s])\S{8,}$")

DUMMY_TEXT1 = '''
Sequi voluptatem vel sit delectus necessitatibus ea nihil reprehenderit. Voluptatem aut perspiciatis ut molestiae perspiciatis porro totam. Temporibus excepturi corporis vel alias quidem. Excepturi beatae et dignissimos excepturi sequi repudiandae omnis. Blanditiis et ipsam officiis neque recusandae qui non qui.'''

DUMMY_TEXT2 = '''
Omnis error dolor consequatur quia sunt quasi. Iure necessitatibus nobis natus hic incidunt officia. Rerum est non nemo laborum. Necessitatibus in assumenda pariatur saepe temporibus nostrum error eveniet. Dolorum quo dolores quaerat aut nulla laudantium excepturi et. Non in temporibus sunt.

Est voluptas voluptas voluptate voluptatibus ratione et ducimus et. Quos odio est occaecati possimus quia quaerat eveniet. Nihil veritatis est repellendus dolor beatae. Voluptatibus non corporis quas ratione fugit qui.

Est magnam dolor similique molestiae et dolores. Et odio totam ea. Quia repellat eos distinctio cum autem dignissimos nemo. Praesentium et ipsam at a consectetur aut id.

Delectus iusto non molestias. Deleniti placeat error sint nulla. Illum minus quos non ut.

Consectetur dicta suscipit culpa. Saepe molestias ut sed ad. Cupiditate aut voluptas veritatis accusantium. Ut assumenda praesentium itaque est voluptatem aut dolorem sunt. Eos occaecati hic enim tempora enim voluptates doloribus est. Nihil laudantium eum eius illum est animi quia aspernatur.
'''

DUMMY_TEXT3 = '''
Aut necessitatibus rerum voluptatum. Illo id alias et modi quod. Dolores et voluptas consequuntur perspiciatis aspernatur labore. Quo vero blanditiis fugiat ipsam sit quo iste consequatur. A perspiciatis rerum sed eum. Ex aut doloremque qui nesciunt consequuntur molestiae.

Sunt quod nesciunt aut quo. Ut quibusdam cupiditate quos molestiae. Ullam perspiciatis ea provident distinctio sunt. Corporis provident natus est omnis repellat aspernatur. Ut vitae ipsam libero et voluptatem corporis. Sequi eaque sint suscipit quis iste consequatur eligendi.

Sed cum velit nisi sed reiciendis ducimus nisi. Saepe aut impedit velit. Qui distinctio fuga natus exercitationem animi aut dolores.

Et ipsa laborum nisi perferendis fuga. Inventore id ut fuga sint id doloremque. Voluptatum qui est voluptate at et sed. Vel ipsa accusantium libero sed vero. Earum provident impedit quas odio vel hic.

Sunt deleniti facere iste eum doloribus. Autem tempore consequatur eos ut nemo sunt dolores. In rerum recusandae ratione facilis officiis sunt. Odit reiciendis qui quam molestiae aspernatur.

Est laboriosam eaque amet. Exercitationem nihil est sapiente ut magnam fuga eum. Quia ut amet porro. Quos qui eveniet quidem sint ut soluta inventore. Nemo officia quis et et.

Voluptatem voluptatem consequuntur earum. Vero porro asperiores ratione. Maiores repellendus eum nemo. Iure nihil consequatur autem autem modi facilis.

Doloremque laboriosam mollitia necessitatibus quo explicabo voluptatum deleniti consequuntur. Adipisci aut neque sapiente doloribus incidunt dignissimos. Voluptas velit quia accusamus tempora. Consectetur et et laudantium ea dignissimos explicabo error. Consequatur mollitia asperiores ut vitae perspiciatis. Harum exercitationem repellat in nihil.

Sunt consequatur repudiandae reprehenderit unde doloremque commodi molestias non. Est at aut recusandae aut eveniet similique. Consequatur officiis sit provident vel doloribus sequi. Quidem fuga velit possimus ad nam corrupti consequatur. Voluptates sit quisquam omnis. Qui ut sit et rerum consequatur.

In est odio fuga qui eaque non dolor. Dolor quae delectus reprehenderit et fugiat sit. Repudiandae maiores quos eos illum et. Et nostrum ut vitae non.
'''